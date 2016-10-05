#define _CRT_SECURE_NO_WARNINGS

#define PROGRAM_FILE "/Users/yaoxiao/Documents/testopencl/testopencl/stump.cl"
#define KERNEL_FUNC "stump"
#define num_features 1000
#define num_data 1024

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#include <OpenCL/cl.h>
#include <time.h>
#include <sys/time.h>

int main() {
    
    time_t start;
    time ( &start );

    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_int i, j, k, err;
    
    cl_program program;
    FILE *program_handle;
    char *program_buffer;
    size_t program_size;
    cl_kernel kernel;
    
    int mat_size = num_features*num_data;
    float mat[mat_size], vec[num_data];
    int result[mat_size];
    
    
    cl_mem mat_buff, vec_buff, res_buff;
    size_t work_units_per_kernel[1];
    
    
    
    for(i=0; i<mat_size; i++) {
        mat[i] = i * 2.0f;
        result[i] = 0;
    }

    for(i=0; i<num_data; i++){
        vec[i] = rand()%2*2.0f-1.0f;
    }
    
    
    clGetPlatformIDs(1, &platform, NULL);
    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    program_handle = fopen(PROGRAM_FILE, "r");
    fseek(program_handle, 0, SEEK_END);
    program_size = ftell(program_handle);
    rewind(program_handle);
    program_buffer = (char*)malloc(program_size + 1);
    program_buffer[program_size] = '\0';
    fread(program_buffer, sizeof(char), program_size, program_handle);
    fclose(program_handle);
    
    program = clCreateProgramWithSource(context, 1,
                                        (const char**)&program_buffer, &program_size, &err);
    free(program_buffer);
    
    clBuildProgram(program, 0, NULL, NULL, NULL, NULL);

    kernel = clCreateKernel(program, KERNEL_FUNC, &err);

    mat_buff = clCreateBuffer(context, CL_MEM_READ_ONLY |
                              CL_MEM_COPY_HOST_PTR, sizeof(float)*mat_size, mat, &err);

    vec_buff = clCreateBuffer(context, CL_MEM_READ_ONLY |
                              CL_MEM_COPY_HOST_PTR, sizeof(float)*num_data, vec, NULL);
    res_buff = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
                              sizeof(int)*mat_size, NULL, NULL);
    
    clSetKernelArg(kernel, 0, sizeof(cl_mem), &mat_buff);
    clSetKernelArg(kernel, 1, sizeof(cl_mem), &vec_buff);
    clSetKernelArg(kernel, 2, sizeof(cl_mem), &res_buff);
    queue = clCreateCommandQueue(context, device, 0, &err);
    work_units_per_kernel[0] = mat_size;
    clEnqueueNDRangeKernel(queue, kernel, 1, NULL, work_units_per_kernel,
                                 NULL, 0, NULL, NULL);
    
    clEnqueueReadBuffer(queue, res_buff, CL_TRUE, 0, sizeof(int)*mat_size,
                              result, 0, NULL, NULL);
    

//    for(i=0;i<mat_size;i++){
//        float current = mat[i];
//        j = i/(int)num_features*(int)num_features;
//        int tmp = 0;
//        for(k=0;k<num_data;k++){
//            if((mat[j+k]-current)*vec[k] > 0.0f){
//                tmp += 1;
//            }
//        }
//        result[i] = tmp;
//    }
    
    int tmp_max = result[0];
    int max_index = 0;
    for(i=0; i<mat_size; i++){
        if(result[i]>tmp_max){
            tmp_max = result[i];
            max_index = i;
        }
    }
    
    printf("optimal feature index is: %d\n",max_index/num_features);
    printf("optimal threshold is: %f\n",mat[max_index]);
    
    clReleaseMemObject(mat_buff);
    clReleaseMemObject(vec_buff);
    clReleaseMemObject(res_buff);
    clReleaseKernel(kernel);
    clReleaseCommandQueue(queue);
    clReleaseProgram(program);
    clReleaseContext(context);
    
    time_t end;
    time ( &end );

    printf("The time spent (in sec) is: %ld\n", end-start);
    
    
    
    
    
    return 0;
}

