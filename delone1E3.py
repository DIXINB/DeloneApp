import cv2
import numpy as np
#import random

#Check if the vertex of the triangle belongs to the contour
def cont1_contains(cont1, point) :
    condition = cont1 == point      
    r=np.any(condition)
    return r

ind=[]

# Draw a point
def draw_point(img, p, color ) :
    cv2.circle( img, p, 3, color, cv2.FILLED, cv2.LINE_AA, 0 )
  
# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :
    triangleList = subdiv.getTriangleList();
    
    for index,t in enumerate(triangleList) :
               
        pt1 = [t[0], t[1]]
        cnd1=cont1_contains(contours_scrap_in, pt1)
               
        pt2 = [t[2], t[3]]
        cnd2=cont1_contains(contours_scrap_in, pt2)
        		
        pt3 = [t[4], t[5]]
        cnd3=cont1_contains(contours_scrap_in, pt3)
        	
        #check that all three vertices of the triangle belong to the contour
        cnd=cnd1 and cnd2 and cnd3
        
                
        if cnd :
            ind.append(index)
         			     
    #remove unnecessary triangle
    triangleList = np.delete(triangleList,(ind),axis=0)
    		
    #draw triangles on the new list
    new_triangleList = triangleList	
    for t in new_triangleList :
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])  
        cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
        cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
        cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
	
if __name__ == '__main__':
 
    # Define window names
    win_delaunay = "Delaunay Triangulation"
     
    # Turn on animation while drawing triangles
    animate = True
     
    # Define colors for drawing.
    delaunay_color = (255,255,255)
    points_color = (0, 0, 255)
 
    # Read in the image.
    
    img = cv2.imread("1m.png") 
    # Keep a copy around
    img_orig = img.copy();
     
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
     
    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect);
    
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, t_image = cv2.threshold(gray_image, 95, 255, 0)
    
	#we search for contours and build their hierarchy
    contours, hierarchy = cv2.findContours(t_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("contours:", type(contours))
    print("hierarchy:", hierarchy)
    #print("CONTOURS[:].SHAPE",contours[0].shape,contours[1].shape,contours[2].shape,contours[3].shape)
    
	
    if contours[0].shape[0]%2 :
        step0 = 12
    else :
        step0 = 11
		
    if contours[1].shape[0]%2 :
        step1 = 12
    else :
        step1 = 11
		
       
    contours_scrap_gl = contours[0][::step0,0,:]
    contours_scrap_in = contours[1][::step1,0,:]
    imax=len(contours)
    print("imax", imax)
    #choose the step with which we will select points for triangulation
    for i in range(1,imax) :
        if contours[i].shape[0]%2 :
            step0 = 12
        else :
            step0 = 11
		#form truncated inner contours
        contours_scrap = contours[i][::step0,0,:]
        #we form a global contour for triangulation
        contours_scrap_gl = np.concatenate((contours_scrap_gl,contours_scrap),axis=0)    
        if i>1 :
        #we form a global internal contour for the destruction of triangles in the "holes"
            contours_scrap_in = np.concatenate((contours_scrap_in,contours_scrap),axis=0)   
	    
    points_tuple = [tuple(map(int,row)) for row in contours_scrap_gl]
	
	#preparing the global contour for triangulation
    contours_scrap_gl_mod=np.reshape(contours_scrap_gl, (1,-1,1,2),order='C')	
    print("contours_scrap_gl_mod:",contours_scrap_gl_mod.shape)
	# Insert points into subdiv
    for p in contours_scrap_gl_mod  :
        subdiv.insert(p)
        print("subdiv",subdiv)

		
        # Show animation
        if animate :
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay( img_copy, subdiv, (0, 255, 255) );
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)
 
    # Draw delaunay triangles
    draw_delaunay( img, subdiv, (0, 255, 0) );
 
    # Draw points
    for p in points_tuple :
       draw_point(img, p, (0,0,255))
 
    # Show results
    cv2.imshow(win_delaunay,img)
    
    cv2.waitKey(0)
