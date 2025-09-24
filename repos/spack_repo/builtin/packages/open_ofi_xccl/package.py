# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class OpenOfiXccl(AutotoolsPackage):
    """TODO Open OFI XCCL is a plug-in which enables EC2 developers to use
    libfabric as a network provider while running NVIDIA's NCCL based
    applications."""

    homepage = "https://github.com/HewlettPackard/open-ofi-xccl"
    url = "https://github.com/HewlettPackard/open-ofi-xccl/archive/v0.0.0.tar.gz"
    # git = "https://github.com/HewlettPackard/open-ofi-xccl.git"
    git = "https://github.com/ryanhankins/open-ofi-xccl.git"

    maintainers("msimberg")

    version("v1.14.x-xccl", branch="v1.14.x-xccl")

    variant("trace", default=False, description="Enable printing trace messages")
    variant("tests", default=False, description="Build tests")
    variant("cuda", default=False, description="Build with CUDA support")
    variant("rocm", default=False, description="Build with ROCm support")

    depends_on("c", type="build")
    # depends_on("cxx", type="build", when="@1.15:")

    depends_on("libfabric")
    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+rocm")
    conflicts("+cuda +rocm")
    # depends_on("nccl")
    depends_on("mpi", when="+tests") # ?
    depends_on("hwloc")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    # def url_for_version(self, version):
    #     if version < Version("1.7.0") or version >= Version("1.14.0"):
    #         return super().url_for_version(version)
    #     url_fmt = "https://github.com/aws/aws-ofi-nccl/archive/v{0}-aws.tar.gz"
    #     return url_fmt.format(version)

    # To enable this plug-in to work with NCCL/RCCL add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.append_path("LD_LIBRARY_PATH", self.prefix.lib)

    # To enable this plug-in to work with NCCL/RCCL add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        env.append_path("LD_LIBRARY_PATH", self.prefix.lib)

    def configure_args(self):
        args = []

        # Always set configure's external paths to use the Spack
        # provided dependencies
        args.extend(
            [
                "--with-libfabric={0}".format(self.spec["libfabric"].prefix),
                "--with-hwloc={0}".format(self.spec["hwloc"].prefix),
                # "--with-nccl={0}".format(self.spec["nccl"].prefix), #?
            ]
        )

        args.extend(self.enable_or_disable("trace"))
        args.extend(self.enable_or_disable("tests"))

        if self.spec.satisfies("+cuda"):
            args.append("--with-cuda={0}".format(self.spec["cuda"].prefix))

        if self.spec.satisfies("+rocm"):
            args.append("--with-hip={0}".format(self.spec["hip"].prefix))

        if self.spec.satisfies("+tests"):
            args.append("--with-mpi={0}".format(self.spec["mpi"].prefix))

        return args
