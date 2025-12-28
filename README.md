# SDXL to NewBie XML Converter

A ComfyUI custom node that converts SDXL-style prompt inputs into the structured XML format required by NewBie models.

## Description

This node allows you to input various prompt components (gender, appearance, clothing, action, etc.) and automatically generates a properly formatted XML string for NewBie checkpoint generation. It simplifies the process of creating complex XML prompts by handling the structure and tags for you.


<img width="1135" height="813" alt="image" src="https://github.com/user-attachments/assets/dce6437c-40b8-4f56-81fd-b2cd2c0ce52c" />



## Features

- **Granular Inputs**: Separate fields for character details, background, style, artist, etc.
- **XML Structuring**: Automatically wraps inputs in `<character_1>`, `<general_tags>`, `<style>`, etc.
- **Auto-Cleaning**: Cleans up formatting issues like extra spaces or newlines.
- **Boilerplate Option**: Optionally adds standard high-quality boilerplate tags.
- **Negative Prompt**: Returns a specialized negative prompt for this workflow.

## Installation

1. Clone this repository into your ComfyUI `custom_nodes` directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/kazama01/SDXL2NewBie.git
   ```
2. Restart ComfyUI.

## Usage

1. Search for the node **"SDXL to NewBie Converter"** in the ComfyUI node menu.
2. Connect string primitives or text widgets to the inputs.
3. The node outputs:
   - `newbie_prompt`: The formatted XML string.
   - `negative_prompt`: A pre-configured negative prompt string.

## Inputs

- `add_boilerplate` (Boolean): Appends standard quality tags (`max_high_resolution`, `masterpiece`, etc.) if enabled.
- `character_gender`: e.g., "1girl"
- `character_appearance`: e.g., "blue eyes, long hair"
- `character_clothing`: e.g., "school uniform"
- `character_action`: e.g., "standing"
- `character_position`: e.g., "looking at viewer"
- `background`: e.g., "classroom"
- ... and more.

