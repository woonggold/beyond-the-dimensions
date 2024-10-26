from settings import *

#이중 적분 느낌? 선형 보간
def lerp( p1, p2, f ):
    return p1 + f * (p2 - p1)

def lerp2d( p1, p2, f ):
    return tuple( lerp( p1[i], p2[i], f ) for i in range(2) )

def draw_quad( image_name, quad ):
    img = pygame.image.load(f"{script_dir}//images//{image_name}.png").convert_alpha()

    points = dict()

    for i in range( img.get_size()[1]+1 ):
        b = lerp2d( quad[1], quad[2], i/img.get_size()[1] )
        c = lerp2d( quad[0], quad[3], i/img.get_size()[1] )
        for u in range( img.get_size()[0]+1 ):
            a = lerp2d( c, b, u/img.get_size()[0] )
            points[ (u,i) ] = a

    for x in range( img.get_size()[0] ):
        for y in range( img.get_size()[1] ):
            color = img.get_at((x,y))
            if color[3] > 0:  # 알파 값이 0이 아닌 경우만 그리기
                pygame.draw.polygon(
                    screen,
                    color,
                    [ points[ (a,b) ] for a, b in [ (x,y), (x,y+1), (x+1,y+1), (x+1,y) ] ] 
                )
#     draw_quad( "시작1", ( (300,300), (600,450), (600,600), (400,600) ))