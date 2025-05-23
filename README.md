# olmOCR on Biowulf

# olmOCR Install

Well... uv doesn't play nice with pip's `--find-links` install for `olmOCR[gpu]` package. No way to record this in pyproject.toml that I know of.

 So... after using uv to set up a python 3.11 venv, Josh ran:

```bash
uv pip install olmocr[gpu] --find-links=https://flashinfer.ai/whl/cu124/torch2.4/flashinfer/
```

as stated in the [olmOCR GitHub README.md](https://github.com/allenai/olmocr)

Triton requires setuptools, which doesn't come with uv pip, so Josh added it, then ran

```bash
uv pip freeze > requirements.txt
```

to make life easier. 
