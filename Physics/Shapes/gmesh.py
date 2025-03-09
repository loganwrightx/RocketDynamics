import gmsh

gmsh.initialize()
gmsh.clear()
gmsh.model.add("rocket")

cyl = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, 1, 0.1)
cone = gmsh.model.occ.addCone(0, 0, 1, 0, 0, 0.5, 0.1, 0)
fused, _ = gmsh.model.occ.fuse([(3, cyl)], [(3, cone)])

gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

gmsh.model.mesh.setSize(gmsh.model.getEntities(), 0.01)
gmsh.model.mesh.generate(2)  # Stop at 2D

node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()

print(node_tags)
print(node_coords)
#gmsh.fltk.run()  # Open GUI

gmsh.finalize()