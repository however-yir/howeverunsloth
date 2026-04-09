#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <version>"
  exit 1
fi

VERSION="$1"
TAG="v${VERSION}"

git fetch --tags >/dev/null 2>&1 || true
if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "tag already exists: $TAG"
  exit 1
fi

git tag -a "$TAG" -m "release ${TAG}"
echo "created tag: $TAG"
echo "push with: git push origin $TAG"
