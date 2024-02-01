// use ferris_says::say; // from the previous step
use std::io::{stdout, BufWriter};

fn main() {
    let stdout = stdout();
    let message = String::from("Hello fellow Rustaceans!");
    let width = message.chars().count();

    let mut writer = BufWriter::new(stdout.lock());
    ferris_says::say(&message, width, &mut writer).unwrap();
}

/*
ERROR: /home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rules_rust/util/process_wrapper/BUILD.bazel:31:36: Compiling Rust (without process_wrapper) bin process_wrapper (6 fi
les) [for tool] failed: (Exit 1): process_wrapper.sh failed: error executing command (from target @rules_rust//util/process_wrapper:process_wrapper) bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/pro
cess_wrapper/process_wrapper.sh -- ... (remaining 21 arguments skipped)                                   
                                                                                                          
Use --sandbox_debug to see verbose messages from the sandbox and retain the sandbox build root for debugging                                                                                                        
error: linking with `external/gcc_toolchain_x86_64/bin/gcc` failed: exit status: 127                                                                                                                                
  = note: LC_ALL="C" PATH="/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/bi
n" VSLANG="1033" "external/gcc_toolchain_x86_64/bin/gcc" "-m64" "/tmp/rustccSpiSS/symbols.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a6
2c4dab-cgu.00.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.01.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rule
s_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.02.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62
c4dab-cgu.03.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.04.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules
_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.05.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c
4dab-cgu.06.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.07.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_
rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.08.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4
dab-cgu.09.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.10.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_r
ust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.11.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4d
ab-cgu.12.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.13.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_ru
st/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4dab-cgu.14.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.process_wrapper.f08ac887a62c4da
b-cgu.15.rcgu.o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper.gkf5n1p5osl7kwu.rcgu.o" "-Wl,--as-needed" "-L" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rust_linux
_x86_64__x86_64-unknown-linux-gnu__stable_tools/rust_toolchain/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-L" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust_tinyjson" "-L" "/home/mchristen/.cache/bazel/_
bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-Wl,-Bstatic" "/home/mchristen/.cache/bazel/_bazel_mc
hristen/eabc9c58e7a2790b61df5bad4df6e1e8/execroot/mchristen/bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust_tinyjson/libtinyjson-4031717389.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2
790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libstd-6498d8891e016dca.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c
58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libpanic_unwind-3debdee1a9058d84.rlib" "/home/mchristen/.cache/bazel/_bazel_m
christen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libobject-8339c5bd5cbc92bf.rlib" "/home/mchristen/.cache/bazel
/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libmemchr-160ebcebb54c11ba.rlib" "/home/mchristen/.ca
che/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libaddr2line-95c75789f1b65e37.rlib" "/home/m
christen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libgimli-7e8094f2d6258832.rlib" 
"/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/librustc_demangle-bac978
3ef1b45db0.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libstd_
detect-a1cd87df2f2d8e76.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gn
u/lib/libhashbrown-7fd06d468d7dba16.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unkn
own-linux-gnu/lib/librustc_std_workspace_alloc-5ac19487656e05bf.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_t
ools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libminiz_oxide-c7c35d32cf825c11.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux
-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libadler-c523f1571362e70b.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unkno
wn-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libunwind-85f17c92b770a911.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86
_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcfg_if-598d3ba148dadcea.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x8
6_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/liblibc-a58ec2dab545caa4.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_l
inux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/liballoc-f9dda8cca149f0fc.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/externa
l/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/librustc_std_workspace_core-7ba4c315dd7a3503.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a27
90b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcore-5ac2993e19124966.rlib" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c
58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcompiler_builtins-df2fb7f50dec519a.rlib" "-Wl,-Bdynamic" "-lgcc_s" "-lutil
" "-lrt" "-lpthread" "-lm" "-ldl" "-lc" "-Wl,--eh-frame-hdr" "-Wl,-z,noexecstack" "-L" "/home/mchristen/.cache/bazel/_bazel_mchristen/eabc9c58e7a2790b61df5bad4df6e1e8/external/rust_linux_x86_64__x86_64-unknown-li
nux-gnu__stable_tools/lib/rustlib/x86_64-unknown-linux-gnu/lib" "-o" "bazel-out/k8-opt-exec-2B5CBBC6/bin/external/rules_rust/util/process_wrapper/process_wrapper" "-Wl,--gc-sections" "-pie" "-Wl,-z,relro,-z,now" 
"-Wl,-O1" "-Wl,--strip-debug" "-nodefaultlibs" "-ldl" "-lpthread" "-Wl,-z,relro,-z,now" "-pass-exit-codes" "-lm" "-lstdc++" "-Wl,--gc-sections" "--sysroot" "external/sysroot_x86_64" "-Bexternal/gcc_toolchain_x86_
64/bin" "-Bexternal/sysroot_x86_64//usr/lib" "-Bexternal/sysroot_x86_64//lib64" "-Lexternal/sysroot_x86_64//lib64" "-Lexternal/sysroot_x86_64//usr/lib" "-Lexternal/sysroot_x86_64//lib/gcc/x86_64-linux/10.3.0"    
  = note: external/gcc_toolchain_x86_64/bin/gcc: line 24: realpath: command not found                     
          external/gcc_toolchain_x86_64/bin/gcc: line 24: dirname: command not found                                                                                                                                
          external/gcc_toolchain_x86_64/bin/gcc: line 24: realpath: command not found
          */
