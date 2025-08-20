from PIL import Image

# Charger l'image originale
img = Image.open("logo.png").convert("RGBA")

# Couleur de fond approximative à supprimer
target_color = (91, 110, 125)  # exemple
threshold = 10  # tolérance

# Préparer les nouveaux pixels
datas = img.getdata()
newData = []

for item in datas:
    r, g, b, a = item
    # Calculer la distance euclidienne
    distance = ((r - target_color[0])**2 + (g - target_color[1])**2 + (b - target_color[2])**2)**0.5
    if distance < threshold:
        newData.append((255, 255, 255, 0))  # transparent
    else:
        newData.append(item)

# Appliquer les modifications
img.putdata(newData)

# Sauvegarder l'image transparente
img.save("logo_transparent.png", "PNG")
print("Logo avec fond transparent créé : logo_transparent.png")
