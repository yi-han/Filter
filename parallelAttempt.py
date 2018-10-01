from mpi4py import MPI

"""
You can check out https://github.com/resbaz/spartan-examples/tree/master/Python/mpi4py-examples-master
for better parraelel stuff

My idea was to run each ddqn agent in parralel. We might be abusing MPI if we
proceed with this idea though, unlikely though

My actual concern and reason why we've (temporaily?) stopped with this endevour
is that it won't scale well. Whilst I've got unlimited time I dont have unlimited nodes

3 hosts is probably fine but pushing it, I might want to try 7 hosts. This would involve
having to do a mixmatch of approaches so better to do the one that involves just time which
is fine.
"""


print("hello")
comm = MPI.COMM_WORLD

rank = comm.Get_rank()

if rank == 0:
    for i in range(comm.size):


comm.Barrier()   # wait for everybody to synchronize _here_