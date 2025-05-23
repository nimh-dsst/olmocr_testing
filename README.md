# olmOCR on Biowulf

Prior to running any olmOCR code ensure you first load poppler tools by:

```bash
module load libpoppler
```

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

## RAM issue

An `sinteractive --gres=gpu:a100:1` instance did not have sufficient RAM to deal with model. Going to try again with

```bash
sinteractive --mem=32g --gres=gpu:a100:1
```

as 16 GB was NOT enough for a test run and the process got killed 💀

## Squid proxy issue

The sglang server need to spin up on localhost, on default port `30024`, in order for the `olmocr.pipeline` CLI to work. However, by default all the web traffic goes through the squid proxy, including the localhost. You have to disable the proxy for localhost by:

```bash
   export NO_PROXY=localhost,127.0.0.1
```

That allows requests to and from the localhost port.
