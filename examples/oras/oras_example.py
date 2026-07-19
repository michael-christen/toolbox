"""Experiment with ORAS (OCI Registry As Storage) for firmware management.

Demonstrates pushing and pulling a simulated RP2040 firmware blob to/from a
local OCI registry, with metadata annotations for versioning and provenance.

Requires a local OCI registry running on localhost:5000:
    docker run -d -p 5000:5000 --name oras-registry registry:2

Evaluate:
- Push/pull firmware blobs with standard OCI tooling
- Attach metadata (version, target, build config) as OCI annotations
- Verify artifact integrity via digest
"""

import hashlib
import struct
import tempfile
from pathlib import Path

import oras.client
import requests

REGISTRY = "localhost:5000"
REPO = f"{REGISTRY}/firmware/rp2040-blinky"
TAG = "v1.0.0"
REF = f"{REPO}:{TAG}"

# OCI media type for raw firmware binaries
MEDIA_TYPE_FIRMWARE = "application/vnd.firmware.bin"
# Config media type (OCI convention for "no config")
MEDIA_TYPE_CONFIG = "application/vnd.oci.empty.v1+json"


def _make_fake_uf2(path: Path, size_kb: int = 16) -> None:
    """Write a minimal UF2-like binary (magic bytes + zero-padded payload)."""
    # UF2 magic numbers from https://github.com/microsoft/uf2
    MAGIC_START0 = 0x0A324655
    MAGIC_START1 = 0x9E5D5157
    MAGIC_END = 0x0AB16F30

    with path.open("wb") as f:
        for block_num in range(size_kb):
            f.write(struct.pack("<I", MAGIC_START0))
            f.write(struct.pack("<I", MAGIC_START1))
            f.write(struct.pack("<I", 0x00002000))  # flags
            f.write(
                struct.pack("<I", 0x10000000 + block_num * 256)
            )  # target addr
            f.write(struct.pack("<I", 256))  # payload size
            f.write(struct.pack("<I", block_num))  # block number
            f.write(struct.pack("<I", size_kb))  # total blocks
            f.write(struct.pack("<I", 0xE48BFF56))  # RP2040 family ID
            f.write(b"\xcc" * 256)  # payload (fake instructions)
            f.write(b"\x00" * (476 - 256))  # padding to 476 bytes
            f.write(struct.pack("<I", MAGIC_END))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def push_firmware(client: oras.client.OrasClient, firmware_path: Path) -> str:
    digest_before = _sha256(firmware_path)
    size = firmware_path.stat().st_size
    print(
        f"Pushing {firmware_path.name}  "
        f"({size} bytes, sha256:{digest_before[:16]}…)"
    )

    annotations = {
        "org.opencontainers.image.version": TAG,
        "dev.toolbox.firmware.target": "rp2040",
        "dev.toolbox.firmware.format": "uf2",
        "dev.toolbox.firmware.size_bytes": str(size),
        "dev.toolbox.firmware.sha256": digest_before,
        "dev.toolbox.build.app": "blinky",
        "dev.toolbox.build.config": "release",
    }

    result = client.push(
        files=[str(firmware_path)],
        target=REF,
        manifest_annotations=annotations,
        disable_path_validation=True,
    )
    print(f"Pushed → {REF}")
    print(f"  manifest digest: {result}")
    return digest_before


def pull_firmware(client: oras.client.OrasClient, out_dir: Path) -> Path:
    print(f"\nPulling {REF} …")
    result = client.pull(target=REF, outdir=str(out_dir))
    print(f"  pulled files: {result}")
    pulled = list(out_dir.iterdir())
    if not pulled:
        raise RuntimeError("Pull returned no files")
    return pulled[0]


def verify(original_digest: str, pulled_path: Path) -> None:
    pulled_digest = _sha256(pulled_path)
    print("\nVerification:")
    print(f"  original sha256 : {original_digest}")
    print(f"  pulled   sha256 : {pulled_digest}")
    if original_digest == pulled_digest:
        print("  PASS — digests match")
    else:
        raise RuntimeError("FAIL — digest mismatch!")


def inspect_manifest() -> None:
    """Query annotations via the OCI Distribution Spec HTTP API."""
    print(f"\nManifest annotations for {REF}:")
    url = f"http://{REGISTRY}/v2/firmware/rp2040-blinky/manifests/{TAG}"
    headers = {"Accept": "application/vnd.oci.image.manifest.v1+json"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    manifest = resp.json()
    annotations = manifest.get("annotations", {})
    for k, v in sorted(annotations.items()):
        print(f"  {k}: {v}")


def main() -> None:
    client = oras.client.OrasClient(insecure=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        firmware = tmp / "blinky-rp2040.uf2"
        _make_fake_uf2(firmware)

        original_digest = push_firmware(client, firmware)

        pull_dir = tmp / "pulled"
        pull_dir.mkdir()
        pulled = pull_firmware(client, pull_dir)

        verify(original_digest, pulled)
        inspect_manifest()

    print("\nExperiment complete.")
    print("Key findings:")
    print("  - oras.client.OrasClient provides a simple push/pull API")
    print("  - OCI annotations carry provenance metadata alongside the blob")
    print("  - Blob integrity guaranteed by OCI content-addressable store")
    print("  - Any OCI-compatible registry (GHCR, ECR, GAR) can host firmware")


if __name__ == "__main__":
    main()
