import json

with open('slides.json') as f:
    data = json.load(f)

def slide_set(slideData):

    avatarList = [slideData[av] for av in slideData if "avatar" in av]
    dialogueList = [slideData[diag] for diag in slideData if "dialogue" in diag]
    camera = slideData["camera"]
    # camera_test.position = (camera["X"], camera["Y"], camera["Z"])
    # scene.active_camera = camera
    print avatarList
    print dialogueList

    for avatar in avatarList:

        # avatarObj = scene.objects[avatar["id"]]
        # avatar.visible = True
        # avatar.position.x = backdrop.position.x + avatar["Xoffset"]* 0.002
        # avatar.position.y = backdrop.position.y
        # avatar.position.z = backdrop.position.z + avatar["Yoffset"]* 0.00125

        # if avatar["status"] == "On":
            print avatar["Xoffset"], avatar["Yoffset"], avatar["id"]#

    for dialogue in dialogueList :

        # dialObj = scene.objects[dialogue["id"]]
        # dialObj.visible = True
        # dialObj.position.x = backdrop.position.x + dialogue["Xoffset"]* 0.002
        # dialObj.position.y = backdrop.position.y
        # dialObj.position.z = backdrop.position.z + dialogue["Yoffset"]* 0.00125
        # dialObj.text = location
        if dialogue["status"] == "On":
            print dialogue["Xoffset"], dialogue["Yoffset"], dialogue["id"]


    print camera["X"], camera["Y"], camera["Z"]


slide_set(data["slide_1"])
