import gmsh

gmsh.initialize()
gmsh.clear()
gmsh.model.add("rocket")

gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # 1 = Delaunay
gmsh.model.mesh.generate(3)

cyl = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, 1, 0.1)
cone = gmsh.model.occ.addCone(0, 0, 1, 0, 0, 0.5, 0.1, 0)
fused, _ = gmsh.model.occ.fuse([(3, cyl)], [(3, cone)])

gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.05)
gmsh.model.mesh.generate(2)  # Stop at 2D
gmsh.fltk.run()  # Open GUI

gmsh.finalize()