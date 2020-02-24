Name:           mpi-hello
Version:        1.0
Release:        1%{?dist}
Summary:        MPI hello world
License:        ASL 2.0

BuildRequires:  mpich-devel

%description
An mpi hello world program

%prep
cat > hello.c <<EOF
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
// Initialize the MPI environment
MPI_Init(NULL, NULL);

// Get the number of processes
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);

// Get the rank of the process
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

// Get the name of the processor
char processor_name[MPI_MAX_PROCESSOR_NAME];
int name_len;
MPI_Get_processor_name(processor_name, &name_len);

// Print off a hello world message
printf("Hello world from processor %s, rank %d out of %d processors\n",
processor_name, world_rank, world_size);

// Finalize the MPI environment.
MPI_Finalize();
}
EOF

%build
%_mpich_load
mpicc -o hello hello.c
%_mpich_unload

%install
mkdir -p %{buildroot}%{_bindir}
cp ./hello %{buildroot}%{_bindir}/

%check
%_mpich_load
mpiexec -np 8 ./hello
%_mpich_unload

%files
%{_bindir}/hello

%changelog
