import re

class SDXLToNewBie:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "add_boilerplate": ("BOOLEAN", {"default": True, "label_on": "Enable", "label_off": "Disable"}),
            },
            "optional": {
                "character_gender": ("STRING", {"multiline": True, "default": "", "placeholder": "Gender."}),
                "character_appearance": ("STRING", {"multiline": True, "default": "", "placeholder": "Apperance."}),
                "character_clothing": ("STRING", {"multiline": True, "default": "", "placeholder": "Clothing."}),
                "character_action": ("STRING", {"multiline": True, "default": "", "placeholder": "Action."}),
                "character_position": ("STRING", {"multiline": True, "default": "", "placeholder": "Position."}),
                "background": ("STRING", {"multiline": True, "default": "", "placeholder": "background"}),
                "style": ("STRING", {"multiline": True, "default": "", "placeholder": "style"}),
                "artist": ("STRING", {"multiline": True, "default": "", "placeholder": "artist name"}),
                "objects": ("STRING", {"multiline": True, "default": "", "placeholder": "objects"}),
                "caption": ("STRING", {"multiline": True, "default": "", "placeholder": "Natural language description"}),
                "extra_tags": ("STRING", {"multiline": True, "default": "", "placeholder": "Any other tags (e.g. LoRA triggers)"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("newbie_prompt", "negative_prompt")
    FUNCTION = "convert"
    CATEGORY = "NewBie"

    def convert(self, add_boilerplate, character_gender="", character_appearance="", character_clothing="", character_action="", character_position="", background="", style="", artist="", objects="", caption="", extra_tags=""):
        
        # Helper to join tags if user accidentally used newlines
        def clean(t):
            return ", ".join([x.strip() for x in t.replace("\n", ",").split(",") if x.strip()])

        # Construct XML
        xml_parts = ["{"]
        
        # Character Block
        # If any character traits are present, we create a block. 
        # (Assuming single character 'character_1' for now as per simple mode)
        has_char = any([character_gender, character_appearance, character_clothing, character_action, character_position])
        
        if has_char:
            xml_parts.append(" <character_1>")
            xml_parts.append("  <n>character_1</n>")
            
            if character_gender:
                xml_parts.append(f"  <gender>{clean(character_gender)}</gender>")
            
            if character_appearance:
                xml_parts.append(f"  <appearance>{clean(character_appearance)}</appearance>")
                
            if character_clothing:
                xml_parts.append(f"  <clothing>{clean(character_clothing)}</clothing>")
                
            if character_action:
                xml_parts.append(f"  <action>{clean(character_action)}</action>")
                
            if character_position:
                xml_parts.append(f"  <position>{clean(character_position)}</position>")
                
            xml_parts.append(" </character_1>")

        # General Tags Block
        xml_parts.append(" <general_tags>")
        
        if caption:
            xml_parts.append(f"  <caption>{clean(caption)}</caption>")

        # Artist tags are often put into style or their own tags. 
        # The guide was ambiguous but generally standard XML tags are flexible.
        # We will append artist to style if style exists, or create a style-like entry?
        # Actually, let's treat 'artist' as 'style' or just append to general tags if no specific mapping strictly required.
        # Guide says "combine different artist tags".
        # Let's put it in <style> or a dedicated <artist> if verified.
        # Safe bet: <style> matches "artist tags" often. 
        # Or Just <artist> might be ignored if not trained.
        # Given "NewBie" is XML trained, it might respect <artist>. I'll try that.
        # If not, the user can move it to style.
        if artist:
             xml_parts.append(f"  <artist>{clean(artist)}</artist>")

        if style:
             xml_parts.append(f"  <style>{clean(style)}</style>")
        
        if background:
             xml_parts.append(f"  <background>{clean(background)}</background>")
             
        if objects:
            xml_parts.append(f"  <objects>{clean(objects)}</objects>") # Guessed tag name, or put in extra?
            # Guide has <objects>briefcase</objects> in line 253! So it is valid.

        if extra_tags:
            # "other" tag exists in example: <other>alternate_costume</other>
            # But maybe user wants flat tags?
            # The structure is strict: { <block> ... }
            # So extra tags must be inside a tag.
            # <general_tags> usually contains the rest.
            # We can use <other> or append to end of general block?
            # Let's use <other> for extra tags.
             xml_parts.append(f"  <other>{clean(extra_tags)}</other>")
             
        xml_parts.append("  <quality>high_resolution, detailed</quality>")
        xml_parts.append(" </general_tags>")
        
        xml_parts.append("}")

        # Final Assembly
        final_prompt = "".join(xml_parts)
        
        if add_boilerplate:
            final_prompt += " <resolution>max_high_resolution</resolution> <quality>very_aesthetic, masterpiece, no_text</quality>"

        # Defined Negative Prompt
        neg_prompt = "<e621_tags>furry</e621_tags> <danbooru_tags>furry,english text, chinese text, korean text, speech bubble, dated, logo, signature, watermark, web address, artist name, character name, copyright name, twitter username, low score rate, worst quality, low quality, bad quality, lowres, low res, pixelated, blurry, blurred, compression artifacts, jpeg artifacts, bad anatomy, worst hands, deformed hands, deformed fingers, deformed feet, deformed toes, extra limbs, extra arms, extra legs, extra fingers, extra digits, extra digit, fused fingers, missing limbs, missing arms, missing fingers, missing toes, wrong hands, ugly hands, ugly fingers, twisted hands, abstract, sequence, lineup, 2koma, 4koma, microsoft paint (medium), artifacts, adversarial noise, has bad revision, resized, image sample, low aesthetic, light_particles</danbooru_tags> <resolution>low_resolution</resolution>"

        return (final_prompt, neg_prompt)

NODE_CLASS_MAPPINGS = {
    "SDXLToNewBie": SDXLToNewBie
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SDXLToNewBie": "SDXL to NewBie Converter"
}
