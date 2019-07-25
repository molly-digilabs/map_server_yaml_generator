import pygame 
import math

# simple script to generate the yaml file to go along with your map
# TODO: calc resolution from distances between points
#       get X, Y from image
#       other parameters as inputs

## user parameters to modify:
X = 4800 # width of image in pixels
Y = 3600 # height of image in pixels
resolution = 0.048768 # meters/pixel

pygame.init()
display_surface = pygame.display.set_mode((X, Y )) 
pygame.display.set_caption('Image') 
image = pygame.image.load(r'localization_map.pgm') 
display_surface.blit(image, (0, 0)) 
pygame.display.update()  

num_clicks = 0
print("click origin")
while True:
    for event in pygame.event.get() : 

        if event.type == pygame.QUIT : 
            pygame.quit() 
            quit() 

        if event.type == pygame.MOUSEBUTTONUP:
            num_clicks += 1
            pos = pygame.mouse.get_pos()
            coord = [pos[0], Y - pos[1]]

            if num_clicks == 1:
                origin = coord
                print("click point in x-dir, relative to clicked origin")
            
            elif num_clicks == 2:
                xdir = coord

                x1 = origin[0]
                x2 = xdir[0]

                y1 = origin[1]
                y2 = xdir[1]

                dx = x2 - x1
                dy = y2 - y1

                atan2_angle = math.atan2(dy,dx)
                th = -1*atan2_angle

                # https://en.wikipedia.org/wiki/Rotation_matrix
                xp = math.cos(th)*x1 - math.sin(th)*y1
                yp = math.sin(th)*x1 + math.cos(th)*y1

                # apply resolution
                xpr = xp*resolution
                ypr = yp*resolution

                xx = -1*xpr
                yy = -1*ypr
                yaw = th

                file = open('generated.yaml', 'w')
                file.write("image: localization_map.pgm\n")
                file.write("resolution: " + str(resolution) + "\n")
                file.write("origin: [" + str(xx) + ", " + str(yy) + ", " + str(yaw) + "]\n")
                file.write("negate: 0\n")
                file.write("occupied_thresh: 0.65\n")
                file.write("free_thresh: 0.196\n")
                file.close()
                print("file generated: generated.yaml")

                quit()


        pygame.display.update()  