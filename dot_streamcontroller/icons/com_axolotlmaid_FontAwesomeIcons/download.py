import os
import sh
import shutil
import codecs
import cairo

if __name__ == "__main__":
    if not os.path.exists("Font-Awesome/"):         # Check if the GitHub repo is not there
        print("Downloading GitHub repository...")   
        sh.git.clone("https://github.com/FortAwesome/Font-Awesome")

    # Delete and create "icons" directory
    if os.path.exists("icons/"):
        shutil.rmtree("icons/")
        
    os.mkdir("icons")
    os.mkdir("icons/black")
    os.mkdir("icons/white")

    # Find every icon
    for root, dirs, files in os.walk("Font-Awesome/svgs/"):
        for file in files:
            if file.endswith(".svg"):
                icon = os.path.join(root, file)

                # Copy icon
                shutil.copyfile(icon, "icons/black/" + file)

                # Open icon
                with codecs.open(icon, encoding="utf-8", errors="ignore") as svg:
                    content = svg.read()

                    # Fill with white
                    white_icon_text = content.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" fill="white"')
                    white_icon = open("icons/white/" + file, "w")
                    white_icon.write(white_icon_text)
                    white_icon.close()