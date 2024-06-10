#include "life.h"
#include <pthread.h>
#include <vector>
#include <stdio.h>



void *helper_function(void* arg);


struct ThreadArgs {
    LifeBoard* state;
    LifeBoard* even;
    //LifeBoard* odd;
    int start;
    int stop;
    int steps;
    pthread_barrier_t* barrier;
    char padding[64];
};


struct thread_vect {
    pthread_t thread;
    //go through rows
    int start;
    int stop;
};



void simulate_life_parallel(int threads, LifeBoard &state, int steps) {
    LifeBoard even{state.width(), state.height()};
    //LifeBoard odd{state.width(), state.height()};
    pthread_barrier_t barrier;
    pthread_barrier_init(&barrier, NULL, threads);
    thread_vect *thread_vector = new thread_vect[threads];
    ThreadArgs *args = new ThreadArgs[threads];
    //printf("Steps: %i", steps);
    int row_nums = state.height() / threads;
    int remainder = state.height() % threads;
    int start_row = 0;
    // if(threads != 40){
    //     printf("THREADS = %i\n", threads);
    // printf("rows = %i\n", state.height());}
    

    
    for (int i = 0; i < threads; i++) {
        int rows_this_thread = row_nums;
        
        if (remainder > 0) {
            rows_this_thread++;
            remainder--;
        }

        args[i].state = &state;
        args[i].even = &even;
        if(i == 0){args[i].start = start_row;}
        else{ args[i].start = start_row;}

        args[i].stop = start_row + rows_this_thread;  // the stop row is just start_row + rows_this_thread
        args[i].steps = steps;
        args[i].barrier = &barrier;
        if (i != 0) {
            args[i].start--;
            }
        if (i != threads - 1) {
            args[i].stop++;
        }
        // printf("Start = %i\n", args[i].start);
        // printf("End: %i \n", args[i].stop);

        pthread_create(&thread_vector[i].thread, NULL, helper_function, &args[i]);
        
        start_row += rows_this_thread;  // Update the start_row for the next iteration
}



    for (int i = 0; i < threads; i++) {
        pthread_join(thread_vector[i].thread, NULL);
    }
    

    delete[] thread_vector;
    delete[] args;
    pthread_barrier_destroy(&barrier);
}






void *helper_function(void* arg){
    ThreadArgs* args = (ThreadArgs*)arg;
    LifeBoard* currentBoard = args->state;
    LifeBoard* nextBoard = args->even;
    int start = args->start;
    int stop = args->stop;
    int steps = args->steps;

    //printf("start = %i\n", start);
    for (int step = 0; step < steps; ++step) {
        /* We use the range [1, width - 1) here instead of
        * [0, width) because we fix the edges to be all 0s.
        */
       //printf("Step in loop: %i \n", step);
        for (int y = start+1; y < stop-1; ++y) {
            for (int x = 1; x < currentBoard->width() - 1; ++x) {
                int live_in_window = 0;
                /* For each cell, examine a 3x3 "window" of cells around it,
                * and count the number of live (true) cells in the window. */
                for (int y_offset = -1; y_offset <= 1; ++y_offset) {
                    for (int x_offset = -1; x_offset <= 1; ++x_offset) {
                        if (currentBoard->at(x + x_offset, y + y_offset)) {
                            ++live_in_window;
                        }
                    }
                }
                /* Cells with 3 live neighbors remain or become live.
                Live cells with 2 live neighbors remain live. */
                nextBoard->at(x, y) = (live_in_window == 3 || (live_in_window == 4 && currentBoard->at(x, y)));
            }
        }
        // Swap pointers for currentBoard and nextBoard
        // swap(*currentBoard, *nextBoard);
        //printf("%iid: ",pthread_barrier_wait(args->barrier));
        //printf("try2\n");
        pthread_barrier_wait(args->barrier);
        if(args->start == 0) {
        swap(*currentBoard, *nextBoard);
        }
        
        // Wait for all threads to reach this point
        pthread_barrier_wait(args->barrier);
    }
    
    return NULL;
}
