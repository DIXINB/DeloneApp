
Task.
There is a picture located in the same folder as delone1E3.py. The contour hierarchy contains no more than 2 levels. It looks like holes in areas of arbitrary shape. Delone triangulation must be performed for all areas except holes. 
So, the input file is 1mask.png. At the output we have a list of triangles and their images. 
Execution idea.
After finding the contours and building their hierarchy, we truncate them. To do this, select part of the points through a step. After that, we form two global contours: contours_scrap_gl and contours_scrap_in. All points for constructing Delaunay triangulations are drawn from the primary contour. 
All hole contours are combined into a second global contour. If all three vertices of the triangle lie on the inner contour, we believe that it is located inside the hole and must be removed.
Having a global contour, we will erroneously exclude triangles whose vertices lie on different holes. In this sense, the code needs to be improved.
Unresolved issue.
For 1m.png picture, triangulation is not performed for the whole area.

