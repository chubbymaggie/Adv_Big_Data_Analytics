
__kernel void getpi(__global int* result) {
    
    int i = get_global_id(0);
    
    float rand_x = ((unsigned int)(1103515245 * 23 * i + 12345) % 2147483648) * 1.0f / 2147483647;
    float rand_y = ((unsigned int)(1103515245 * (31 * i + 1) + 12345) % 2147483648) * 1.0f / 2147483647;
    if(rand_x*rand_x+rand_y*rand_y <= 1.0f){
        atomic_inc(result);
    }
}

