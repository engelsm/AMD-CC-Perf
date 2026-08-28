cmake_minimum_required(VERSION 3.10)
project(MA LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_compile_options(-O3)

find_package(OpenMP REQUIRED)

set(EXT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external")

execute_process(
    COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libstdc++.a
    OUTPUT_VARIABLE STATIC_LIBSTDCXX
    OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(
    COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libgcc.a
    OUTPUT_VARIABLE STATIC_LIBGCC
    OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(
    COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libgcc_eh.a
    OUTPUT_VARIABLE STATIC_LIBGCC_EH
    OUTPUT_STRIP_TRAILING_WHITESPACE)

set(STATIC_LIBS
    "-Wl,--start-group"
    "${STATIC_LIBSTDCXX}"
    "${STATIC_LIBGCC}"
    "${STATIC_LIBGCC_EH}"
    "-Wl,-Bstatic" "m" "-Wl,-Bdynamic"
    "-Wl,--end-group"
    "pthread" "c" "dl"
)

add_executable(stream src/stream.c)
target_compile_options(stream PRIVATE -O3 -mcmodel=medium)
target_compile_definitions(stream PRIVATE
    STREAM_ARRAY_SIZE=430080000
    NTIMES=100
)
target_link_libraries(stream PRIVATE
    ${STATIC_LIBS}
    OpenMP::OpenMP_C
)
set_target_properties(stream PROPERTIES LINK_FLAGS "-nodefaultlibs")

set(PROGRAMS
    spmv
    krylov
    preprocess_matrix
    synthgen
    IO_Performance
)

foreach(PROG ${PROGRAMS})
    add_executable(${PROG} src/${PROG}.cpp)

    target_link_libraries(${PROG} PRIVATE
        ${STATIC_LIBS}
        OpenMP::OpenMP_CXX
    )

    set_target_properties(${PROG} PROPERTIES LINK_FLAGS "-nodefaultlibs")

    target_include_directories(${PROG} PRIVATE
        src
        ${EXT_DIR}/spectra/include
        ${EXT_DIR}/fast_matrix_market/include
        ${EXT_DIR}/eigen
    )
endforeach()

add_executable(spmv_DYNAMIC src/spmv.cpp)

target_link_libraries(spmv_DYNAMIC PRIVATE
    OpenMP::OpenMP_CXX
)

target_include_directories(spmv_DYNAMIC PRIVATE
    src
    ${EXT_DIR}/spectra/include
    ${EXT_DIR}/fast_matrix_market/include
    ${EXT_DIR}/eigen
)

target_compile_options(spmv_DYNAMIC PRIVATE -march=native)