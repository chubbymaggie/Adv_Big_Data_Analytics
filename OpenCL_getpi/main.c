#define _CRT_SECURE_NO_WARNINGS
#define PROGRAM_FILE "/Users/yaoxiao/Documents/opencl2/opencl2/getpi.cl"
#define KERNEL_FUNC "getpi"

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
    cl_int i, err;
    
    cl_program program;
    FILE *program_handle;
    char *program_buffer;
    size_t program_size;
    cl_kernel kernel;
    
    int sample_size = 1000000000;
    int result = 0;
    
    cl_mem res_buff;
    size_t work_units_per_kernel;
    
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
    
    
    
    res_buff = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
                              sizeof(int), NULL, NULL);
    
    clSetKernelArg(kernel, 0, sizeof(cl_mem), &res_buff);
    queue = clCreateCommandQueue(context, device, 0, &err);
    
    
    
    work_units_per_kernel = sample_size;
    clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &work_units_per_kernel,
                           NULL, 0, NULL, NULL);
    
    clEnqueueReadBuffer(queue, res_buff, CL_TRUE, 0, sizeof(int),
                        &result, 0, NULL, NULL);
    
    
//    result = 0;
//    for(i=0;i<sample_size;i++){
//        float rand_x = ((unsigned int)(1103515245 * 23 * i + 12345) % 2147483648) * 1.0f / 2147483647;
//        float rand_y = ((unsigned int)(1103515245 * (31 * i + 1) + 12345) % 2147483648) * 1.0f / 2147483647;
//        if(rand_x*rand_x+rand_y*rand_y <= 1.0f){
//            result++;
//        }
//    }
    
    printf("%f\n",4.0f*result/sample_size);

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

