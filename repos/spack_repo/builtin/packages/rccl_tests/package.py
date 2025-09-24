# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class RcclTests(CMakePackage, ROCmPackage):
    """These tests check both the performance and the correctness of RCCL
    operations. They can be compiled against RCCL."""

    homepage = "https://github.com/ROCm/rccl-tests"
    git = "https://github.com/ROCm/rccl-tests.git"
    url = "https://github.com/ROCm/rccl-tests.git"
    tags = ["rocm"]

    maintainers("bvanessen")

    license("BSD-3-Clause")

    version("develop", branch="develop", preferred=True)
    version("master", branch="master")

    variant("mpi", default=True, description="with MPI support")

    depends_on("cxx", type="build")  # generated
    requires("%cxx=llvm-amdgpu")

    conflicts("~rocm")
    depends_on("hip")
    depends_on("rccl")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define("EXPLICIT_ROCM_VERSION", self.spec["hip"].version),
            self.define("ROCM_PATH", self.spec["hip"].prefix),
            self.define("RCCL_ROOT", self.spec["rccl"].prefix),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define("GPU_TARGETS", ";".join(spec.variants["amdgpu_target"].value)),
        ]
        return args
