# CMAKE generated file: DO NOT EDIT!
# Generated by "NMake Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

!IF "$(OS)" == "Windows_NT"
NULL=
!ELSE
NULL=nul
!ENDIF
SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = C:\Users\Ryan\AppData\Local\JetBrains\Toolbox\apps\CLion\ch-0\201.6668.126\bin\cmake\win\bin\cmake.exe

# The command to remove a file.
RM = C:\Users\Ryan\AppData\Local\JetBrains\Toolbox\apps\CLion\ch-0\201.6668.126\bin\cmake\win\bin\cmake.exe -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles\FinalProject.dir\depend.make

# Include the progress variables for this target.
include CMakeFiles\FinalProject.dir\progress.make

# Include the compile flags for this target's objects.
include CMakeFiles\FinalProject.dir\flags.make

CMakeFiles\FinalProject.dir\main.cpp.obj: CMakeFiles\FinalProject.dir\flags.make
CMakeFiles\FinalProject.dir\main.cpp.obj: ..\main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/FinalProject.dir/main.cpp.obj"
	C:\PROGRA~2\MICROS~2\2019\ENTERP~1\VC\Tools\MSVC\1425~1.286\bin\Hostx86\x86\cl.exe @<<
 /nologo /TP $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) /FoCMakeFiles\FinalProject.dir\main.cpp.obj /FdCMakeFiles\FinalProject.dir\ /FS -c E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\main.cpp
<<

CMakeFiles\FinalProject.dir\main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FinalProject.dir/main.cpp.i"
	C:\PROGRA~2\MICROS~2\2019\ENTERP~1\VC\Tools\MSVC\1425~1.286\bin\Hostx86\x86\cl.exe > CMakeFiles\FinalProject.dir\main.cpp.i @<<
 /nologo /TP $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\main.cpp
<<

CMakeFiles\FinalProject.dir\main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FinalProject.dir/main.cpp.s"
	C:\PROGRA~2\MICROS~2\2019\ENTERP~1\VC\Tools\MSVC\1425~1.286\bin\Hostx86\x86\cl.exe @<<
 /nologo /TP $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) /FoNUL /FAs /FaCMakeFiles\FinalProject.dir\main.cpp.s /c E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\main.cpp
<<

# Object files for target FinalProject
FinalProject_OBJECTS = \
"CMakeFiles\FinalProject.dir\main.cpp.obj"

# External object files for target FinalProject
FinalProject_EXTERNAL_OBJECTS =

FinalProject.exe: CMakeFiles\FinalProject.dir\main.cpp.obj
FinalProject.exe: CMakeFiles\FinalProject.dir\build.make
FinalProject.exe: CMakeFiles\FinalProject.dir\objects1.rsp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable FinalProject.exe"
	C:\Users\Ryan\AppData\Local\JetBrains\Toolbox\apps\CLion\ch-0\201.6668.126\bin\cmake\win\bin\cmake.exe -E vs_link_exe --intdir=CMakeFiles\FinalProject.dir --rc=C:\PROGRA~2\WI3CF2~1\10\bin\100183~1.0\x86\rc.exe --mt=C:\PROGRA~2\WI3CF2~1\10\bin\100183~1.0\x86\mt.exe --manifests  -- C:\PROGRA~2\MICROS~2\2019\ENTERP~1\VC\Tools\MSVC\1425~1.286\bin\Hostx86\x86\link.exe /nologo @CMakeFiles\FinalProject.dir\objects1.rsp @<<
 /out:FinalProject.exe /implib:FinalProject.lib /pdb:E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug\FinalProject.pdb /version:0.0  /machine:X86 /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib 
<<

# Rule to build all files generated by this target.
CMakeFiles\FinalProject.dir\build: FinalProject.exe

.PHONY : CMakeFiles\FinalProject.dir\build

CMakeFiles\FinalProject.dir\clean:
	$(CMAKE_COMMAND) -P CMakeFiles\FinalProject.dir\cmake_clean.cmake
.PHONY : CMakeFiles\FinalProject.dir\clean

CMakeFiles\FinalProject.dir\depend:
	$(CMAKE_COMMAND) -E cmake_depends "NMake Makefiles" E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug E:\Chapman\graduate-work\cs-629-data-visualisation\FinalProject\cmake-build-debug\CMakeFiles\FinalProject.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles\FinalProject.dir\depend

