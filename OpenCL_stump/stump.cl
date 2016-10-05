
#define num_features 1000
#define num_data 1024

__kernel void stump(__global float* matrix,
                          __global float* vector,
                          __global int* result) {
    
    int i = get_global_id(0);
    float current = matrix[i];
    int j = i/(int)num_features*(int)num_features;
    int k;
    
    int tmp = 0;
    
    for(k=0;k<num_data;k++){
        if((matrix[j+k]-current)*vector[k] > 0.0f){
            tmp += 1;
        }
    }
        
    result[i] = tmp;
    
}

