```bash
# docs: https://julialang.github.io/PackageCompiler.jl/dev/devdocs/sysimages_part_1/

# set up dependency file deps.jl
# Base.init_depot_path()
# Base.init_load_path()
# using dep1
# using dep2
# empty!(LOAD_PATH)
# empty!(DEPOT_PATH)

# compile object file
julia --startup-file=no --output-o sys.o -J"$(julia -e 'println(unsafe_string(Base.JLOptions().image_file))')" deps.jl

# link shared library
gcc -shared -o sys.dylib -Wl,-all_load sys.o -L"$(julia -e 'println(abspath(Sys.BINDIR, Base.LIBDIR))')" -ljulia

# next: reduce size of library?

# next next: add precompiling...

```