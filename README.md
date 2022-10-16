# i-simpa-vtk
Function to export I-SIMPA csbin data to VTK
It manipulates the content of the csbin results using function from libsimpa and export it into VTK
The script uses the library EVTK to create the VTK files.
Numpy is required to run this script.

After running the case on I-SIMPA, one can export the scene to obtain a .ply of the geometry simulated.
The display can then be refined on Paraview importing both the .ply and the vtk generated using this script.
See Figure below for an exemple of one of I-SIMPA tutorials, converted to VTK using this script and rendered on Paraview. 

<p style="text-align:center;">
<img src="/doc/exemple_paraview_auditorium.png" alt="Paraview Rendering of I-SIMPA Auditorium Tutorial" width="75%" title="Paraview Rendering of after VTK import">
</p>

Link to I-SIMPA https://i-simpa.univ-gustave-eiffel.fr/

Link to EVTK https://github.com/paulo-herrera/PyEVTK

Link to Paraview https://www.paraview.org/
