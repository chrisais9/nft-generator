from PIL import Image
from image4layer import Image4Layer
import yaml
import random
import json


class Generator:

    def __init__(self, config):
        self.traits = []
        self.config = config
        self.final_images = []
        self.width = 2000
        self.height = 2000

    def generate(self):

        self.traits = self.generate_traits()

        if self.is_all_trait_unique(self.traits):
            print("Confirmed that every single trait is unique")
        else:
            print("Error! There are duplicated trait")
            return

        self.generate_all_trait_metadata()

        for trait in self.traits:
            image = self.generate_image(trait)
            image.show()

    def generate_traits(self):
        traits = []
        for i in range(self.config["number"]):
            new_trait = self.new_random_unique_trait()
            traits.append(new_trait)
        return traits

    def new_random_unique_trait(self):
        trait = {}

        traits = self.config["traits"]
        categories = list(traits.keys())
        for category in categories:
            trait[category] = random.choices(
                [k for k in traits[category]["values"].keys()],
                [v["prob"] for v in traits[category]["values"].values()]
            )[0]

        if trait in self.traits:
            return self.new_random_unique_trait()
        else:
            return trait

    def is_all_trait_unique(self, traits):
        seen = list()
        return not any(i in seen or seen.append(i) for i in traits)

    def generate_all_trait_metadata(self):
        METADATA_FILE_NAME = './metadata/all-traits.json'
        with open(METADATA_FILE_NAME, 'w') as outfile:
            json.dump(self.traits, outfile, indent=4)

    def generate_image(self, trait):
        stack = Image.new('RGBA', (self.width, self.height))

        for category, name in trait.items():
            image_layer = Image.open(f'{self.config["traits"][category]["values"][name]["src"]}').convert('RGBA')
            stack = Image.alpha_composite(stack, image_layer)

        filter = Image.open("image/filter.png").convert("RGBA")
        filter.putalpha(int(256 * 0.3))
        stack = Image4Layer.pin_light(stack, filter)

        stack = stack.convert('RGB')
        return stack


def main():
    with open('config.yaml') as config:
        config = yaml.load(config, Loader=yaml.FullLoader)

    # random.seed(config["seed"])

    generator = Generator(config)
    generator.generate()


if __name__ == '__main__':
    main()
