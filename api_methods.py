import discord
import aiohttp
from PIL import Image
from openai import OpenAI

import io
import re
import xml.etree.ElementTree as ET
import random
import os

class api_methods():
    DISCORD_SIZE_LIMIT_BYTES = 10_000_000
    
    def __init__(self, ):
        self.LLM_API_KEY = os.getenv("LLM_KEY")
        self.ENDPOINT = os.getenv("LLM_ENDPOINT")
        self.MODEL_NAME = os.getenv("LLM_MODEL_NAME")
        self.DEPLOYMENT_NAME = os.getenv("LLM_DEPLYMENT_NAME")

        self.ALICE_LLM_client = OpenAI(
            base_url=f"{self.ENDPOINT}",
            api_key=self.LLM_API_KEY
        )


    def resize_image_bytes(self, img_buffer, target_filesize, tolerance=5):
        """reads an image from a buffer and resizes in bytes instead of image dimensions"""
        #TODO: This appears to resize to an acceptable size, but not the maximizing size that could be given
        img = img_orig = Image.open(img_buffer).convert("RGB")

        '''img = Image.new(
            mode="RGB",
            size=(int(img_width), int(img_height))
        )'''
        buffer = img_buffer
        aspect = img.size[0] / img.size[1]

        while True:
            with io.BytesIO() as buffer:
                img.save(buffer, format="JPEG")
                data = buffer.getvalue()
            filesize = len(data)    
            size_deviation = filesize / target_filesize
            print("size: {}; factor: {:.3f}".format(filesize, size_deviation))

            if size_deviation <= (100 + tolerance) / 100:
                # filesize fits
                #print(data)
                return io.BytesIO(data)
            else:
                # filesize not good enough => adapt width and height
                # use sqrt of deviation since applied both in width and height
                new_width = img.size[0] / size_deviation**0.5    
                new_height = new_width / aspect
                # resize from img_orig to not lose quality
                img = img_orig.resize((int(new_width), int(new_height)))


    async def fox_api(self, ctx):
        url = "https://randomfox.ca/floof/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as fox_request:
                if fox_request.status != 200:
                    return await ctx.send(f"Fox API failed with HTTP Status {fox_request.status}")

                fox_json = await fox_request.json()
                fox_image_loc = fox_json['image']
                fox_image_number = re.findall(r'\d+', fox_image_loc)[0]

                async with session.get(fox_image_loc) as fox_image_request:
                    fox_image_data = io.BytesIO(await fox_image_request.read())
                    await ctx.send(file=discord.File(fox_image_data, f"random_fox_{fox_image_number}.jpg"))


    async def furina_api(self, ctx, id_num=None):
        #TODO: Add command options for searching artwork from Safebooru
        random_limit = random.randint(0, 62)
        url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=furina_(genshin_impact)&pid={random_limit}"
        if id_num:
            url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&id={id_num}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as furina_request:
                if furina_request.status != 200:
                    return await ctx.send(f"Safebooru API failed with HTTP Status {furina_request.status}")
            
                furina_xml_data = await furina_request.read()
                root = ET.fromstring(furina_xml_data)

                random_index = random.randint(0, 99)
                if id_num:
                    random_index = 0
                root_post = root.findall("post")[random_index]
                furina_img_loc = root_post.attrib.get("file_url")
                #furina_img_height = (int) (root_post.attrib.get("height"))
                #furina_img_width = (int) (root_post.attrib.get("width"))
                furina_img_number = random_limit * 100 + random_index
                
                async with session.get(furina_img_loc) as furina_image_request:
                    furina_image_data = io.BytesIO(await furina_image_request.read())
                    if len(furina_image_data.getvalue()) >= self.DISCORD_SIZE_LIMIT_BYTES:
                        print(f"Resizing Image {furina_img_number}")
                        furina_image_data = self.resize_image_bytes(furina_image_data, self.DISCORD_SIZE_LIMIT_BYTES)
                    await ctx.send(file=discord.File(furina_image_data, f"random_furina_{furina_img_number}.jpg"))


    async def hu_tao_api(self, ctx, id_num=None):
        #TODO: Add command options for searching artwork from Safebooru
        random_limit = random.randint(0, 66)
        url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=hu_tao_(genshin_impact)&pid={random_limit}"
        if id_num:
            url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&id={id_num}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as hu_tao_request:
                if hu_tao_request.status != 200:
                    return await ctx.send(f"Safebooru API failed with HTTP Status {hu_tao_request.status}")
            
                hu_tao_xml_data = await hu_tao_request.read()
                root = ET.fromstring(hu_tao_xml_data)

                random_index = random.randint(0, 99)
                if id_num:
                    random_index = 0
                root_post = root.findall("post")[random_index]
                hu_tao_img_loc = root_post.attrib.get("file_url")
                #hu_tao_img_height = (int) (root_post.attrib.get("height"))
                #hu_tao_img_width = (int) (root_post.attrib.get("width"))
                hu_tao_img_number = random_limit * 100 + random_index
                
                async with session.get(hu_tao_img_loc) as hu_tao_image_request:
                    hu_tao_image_data = io.BytesIO(await hu_tao_image_request.read())
                    if len(hu_tao_image_data.getvalue()) >= self.DISCORD_SIZE_LIMIT_BYTES:
                        print(f"Resizing Image {hu_tao_img_number}")
                        hu_tao_image_data = self.resize_image_bytes(hu_tao_image_data, self.DISCORD_SIZE_LIMIT_BYTES)
                    await ctx.send(file=discord.File(hu_tao_image_data, f"random_hu_tao_{hu_tao_img_number}.jpg"))


    async def arizona_api(self, ctx):
        ALICE_arizona_response = self.ALICE_LLM_client.chat.completions.create(
            model=self.DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "user",
                    "content": "Within one sentence, write a fun fact about the state of Arizona.",
                }
            ],
        )

        await ctx.send(ALICE_arizona_response.choices[0].message.content)