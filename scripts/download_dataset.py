#!/usr/bin/env python3
"""
Download HackerNoon Tech Company News dataset from Hugging Face.

Dataset:
https://huggingface.co/datasets/HackerNoon/tech-company-news-data-dump

Default:
    Download only cleanedCompanyNews.csv into data/raw/

Requirements:
    pip install -U huggingface_hub

Authentication:
    Option 1 (recommended):
        hf auth login

    Option 2:
        export HF_TOKEN="hf_xxx"

Before downloading, open the dataset page in your browser and accept
the gated-dataset access conditions using the same Hugging Face account.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.errors import GatedRepoError, HfHubHTTPError


REPO_ID = "HackerNoon/tech-company-news-data-dump"
DEFAULT_FILE = "cleanedCompanyNews.csv"
DEFAULT_OUTPUT_DIR = Path("data/raw")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download HackerNoon tech-company-news-data-dump."
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )

    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help=f"File to download. Default: {DEFAULT_FILE}",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Download the entire dataset repository (~6.16 GB).",
    )

    return parser.parse_args()


def get_token() -> str | None:
    """
    HF_TOKEN is optional.

    If it is not set, huggingface_hub automatically uses the token saved
    locally by `hf auth login`.
    """
    return os.getenv("HF_TOKEN")


def download_single_file(
    filename: str,
    output_dir: Path,
    token: str | None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Repository : {REPO_ID}")
    print(f"[INFO] File       : {filename}")
    print(f"[INFO] Output dir : {output_dir.resolve()}")
    print("[INFO] Starting download...")

    path = hf_hub_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        filename=filename,
        token=token,
        local_dir=output_dir,
    )

    return Path(path)


def download_entire_dataset(
    output_dir: Path,
    token: str | None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Repository : {REPO_ID}")
    print(f"[INFO] Output dir : {output_dir.resolve()}")
    print("[INFO] Downloading entire dataset repository...")

    path = snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        token=token,
        local_dir=output_dir,
    )

    return Path(path)


def print_access_help() -> None:
    print(
        """
[ERROR] Hugging Face denied access to the dataset.

This dataset is gated.

Do the following:

1. Open:
   https://huggingface.co/datasets/HackerNoon/tech-company-news-data-dump

2. Log in to Hugging Face.

3. Accept the dataset access/contact-sharing conditions.

4. Authenticate locally:

       hf auth login

   Or set a token:

       export HF_TOKEN="hf_xxxxxxxxxxxxxxxxx"

5. Run this script again.
""",
        file=sys.stderr,
    )


def main() -> int:
    args = parse_args()
    token = get_token()

    try:
        if args.all:
            path = download_entire_dataset(
                output_dir=args.output_dir,
                token=token,
            )
        else:
            path = download_single_file(
                filename=args.file,
                output_dir=args.output_dir,
                token=token,
            )

    except GatedRepoError:
        print_access_help()
        return 1

    except HfHubHTTPError as exc:
        status_code = getattr(exc.response, "status_code", None)

        if status_code in (401, 403):
            print_access_help()
        else:
            print(f"[ERROR] Hugging Face request failed: {exc}", file=sys.stderr)

        return 1

    except KeyboardInterrupt:
        print("\n[INFO] Download interrupted by user.", file=sys.stderr)
        return 130

    except Exception as exc:
        print(f"[ERROR] Download failed: {exc}", file=sys.stderr)
        return 1

    print()
    print("[SUCCESS] Download completed.")
    print(f"[SUCCESS] Saved at: {path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())