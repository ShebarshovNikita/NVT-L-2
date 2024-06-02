import asyncio
from onvif import ONVIFCamera


async def move_camera(camera_ip, camera_port, username, password):

    mycam = ONVIFCamera(camera_ip, camera_port, username, password, """C:\\Users\\root\\Desktop\\All\Course-3\CVT\lab\python-onvif-zeep-async\onvif\wsdl""")
    await mycam.update_xaddrs()

    ptz_service = await mycam.create_ptz_service()

    media_service = await mycam.create_media_service()
    media_profiles = await media_service.GetProfiles()
    media_profile_token = media_profiles[0].token

    request = ptz_service.create_type('AbsoluteMove')
    request.ProfileToken = media_profile_token
    request.Position = {
        'PanTilt': {
            'x': 0.7, 
            'y': 0.7   
        },
        'Zoom': {
            'x': 0.0   
        }
    }
    request.Speed = {
        'PanTilt': {
            'x': 1.0,
            'y': 1.0
        },
        'Zoom': {
            'x': 1.0
        }
    }

    await ptz_service.AbsoluteMove(request)

    return media_profile_token

async def check_position(token): 
    mycam = ONVIFCamera(camera_ip, camera_port, username, password, """C:\\Users\\root\\Desktop\\All\Course-3\CVT\lab\python-onvif-zeep-async\onvif\wsdl""")
    await mycam.update_xaddrs()

    try:
        ptz_service = await mycam.create_ptz_service()
        status = await ptz_service.GetStatus({'ProfileToken': token})
    
        print('Pan', status.Position.PanTilt.x)
        print('Tilt', status.Position.PanTilt.y)
        print('Zoom', status.Position.Zoom.x)
    except Exception as e:
        print("\nPTZ service not supported or error occurred:")
        print(e)




if __name__ == "__main__":

    camera_ip = '172.18.212.18'
    camera_port = 80
    username = 'admin'
    password = 'Supervisor'

    token = asyncio.run(move_camera(camera_ip, camera_port, username, password))
    asyncio.run(check_position(token))