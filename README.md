# Text Parsing of NIMH 2024 Pubs using olmOCR from AI2

## Intro

Oddpub 7.1 uses some sort of something to try and get natural language extracts from PDFs. Unforetunately, it sucks. While Josh Lawrimore, your's truly here, hasn't done a comprehensive examination of the issue, it deleted text from a PDF. No bueno. Initial comparisons of oddpub 5.x and oddpub 7.1 showed much worse correponsdence with each other. I suspect that the dropping of text in the extraction is to blame.

After complaining loudly about the new problem with Oddpub 7.1 to DSST, Adam Thomas heard good thing about AI2's olmOCR from MLT lead, Francisco Pereira. Francisco reasoned that the GPUs on Curium could run the olmOCR model, even on a single GPU. So, here we are, on Curium, giving it a go.

## From HuggingFace 🤗 to Curium ☢️

Josh Lawrimore went ot the [HuggingFace olmOCR Repo](https://huggingface.co/allenai/olmOCR-7B-0225-preview) and used UV to install the [olmocr module](https://github.com/allenai/olmocr). The code in the `main.py` script is derived from the sample code in the [HuggingFace olmOCR Repo](https://huggingface.co/allenai/olmOCR-7B-0225-preview). Initial tests showed that the `paper.pdf` could not be processed. Seems the demo PDF isn't working from the code.

Josh uploaded the olmocr paper as pdf to Curium ☢️ and the demo code in main succeeded in processing, at least part, of the pdf 🎉.

The [olmocr module](https://github.com/allenai/olmocr) contains code to batch convert pdfs in a folder. In order to compare the text extracts from Oddpub 5.x, Oddpub 7.1, olmOCR, and some ground truth (at least for web articles) for NIMH 2024 pubs.

## NIMH 2024 Pubs PDF Corpus 📕

Josh downlaoded the [NIMH_2024_manual_labeling](https://docs.google.com/spreadsheets/d/10TzX1e5-0DyVAczdBqQJyxlpurdfOjQZUgMW_ZSgnfo/edit?usp=sharing) Google Doc as a CSV and used `scp` to put it on Curium ☢️. Josh then converted the PMID list to a unique list of `f"{PMID}.pdf"` strings and serialized that list to the file `nimh_manual_pdfs_2024.json`.

Josh then used Cursor in Agent mode to write the `download_nimh_manual_pdfs.py` to search for the pdf files listed in `nimh_manual_pdfs_2024.json` in the `osm-pdf-uploads` s3 bucket. The log file `nimh_pdf_download_20250522_144802.log` shows 201 files were downloaded with 17 not found in the bucket. This is probably due to stupid cloudflare blocking the files in non-open-access documents. Josh plans on maually downloading the missing PDFs and putting them into the `osm-pdf-uploads` s3 bucket later.

## Download of missing PDFs

38222065.pdf is still embargoed by Taylor and Francis. It's a commentary, not a research article so no need to include it in corpus.

All other missing PDFs were downloaded manually from publisher site and put into `nimh_pdfs_2024` using scp. The 16 missing PDFs were uploaded to the `osm-pdf-uploads` s3 bucket.

## Test run

Josh created a `test_pdfs` folder and put 3 publisher PDFs inside. First attempt at running pipeline failed as it requires [sgland](https://docs.sglang.ai/start/install.html).

### GPU Compute Capability Incompatibility with SGLANG

Whomp whomp 💔. Curium only appears to have 1 GPU, a Quadro P6000, with Compute Capability 6.1. According to Cursor, SGLang needs a newer GPU with compute capability 7.5 or higher (like RTX 20xx series or newer). So... looks like the `pipeline` module included in the `olmocr` repo will not work on Curium. Probably would work on Biowulf with an A100 GPU...

Even a single pdf extract uses the pipeline and needs `sglang`. So it seems we get to write our own inference code... or I try it on BioWulf.


## Meanwhile, on Biowulf

Josh was able to sinteractive into an a100 node and run the same demo code on a pdf. However, could not spin up sglang server on localhost on curium. That may not be allowed. So... yeah... we will need to write our own inference code...
