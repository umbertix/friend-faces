from friendFaces import FriendFaces

try:
    main = FriendFaces()
    while True:
        pass
except KeyboardInterrupt:
    main.color_wipe(main.offColor)
