#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <bits/stdc++.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
using namespace std;

int i_o_interpret(const char * fileName, bool input);

vector<vector<char*>> split_commands(const string& command_line){
    stringstream ss(command_line);
    string temp;
    char* c;
    vector<char*> command;
    vector<vector<char*>> command_list;
    string symbol = "|";
    while(ss >> temp){
        if(temp == symbol){
            if(command.empty()){ //means command line starts with pipeline
                std::cerr << EACCES;
            }
            command.push_back(nullptr);
            if (command.size()>1){
                command_list.push_back(command);
            }
            command.clear();
        }
        else{
            c = new char[temp.size() + 1];
            strcpy(c, temp.c_str());
            command.push_back(c);
            //command.push_back(nullptr);
        }
    }
    if(command.empty()){ // means command line ends with pipeline
        std::cerr << EACCES;
    }

    command.push_back(nullptr);
    command_list.push_back(command);
    return command_list;

}




void pipeline(vector<vector<char*>>& command_list){
    int num_commands = command_list.size();

    int file_descriptors[2]; // File descriptor array
    int in_fd = 0; // input file descripto
    pid_t cpid;

    for(int i = 0; i < num_commands; i++){

        if (pipe(file_descriptors) == -1) {
            std::cerr<<EACCES;
        }

        cpid = fork();

        if (cpid == -1) {
            std::cerr<<EACCES;
        }

        if(cpid == 0) {
            // CHILD
            // Redirecting input
            if(in_fd != 0){
                dup2(in_fd, 0);
                close(in_fd);
            }
            if(i != num_commands - 1){
                dup2(file_descriptors[1], 1);
            }
            close(file_descriptors[0]);
            close(file_descriptors[1]);

            for (size_t j = 0; j < command_list[i].size() - 1; j++) {
                if (strcmp(command_list[i][j], "<") == 0) {
                    if (command_list[i].size()-2 == j){
                        std::cerr << "Invalid command.\n";
                    }
                    i_o_interpret(command_list[i][j+1], true);
                    command_list[i].erase(command_list[i].begin() + j);
                    command_list[i].erase(command_list[i].begin() + j);
                    j--;
                    j--;
                } 
                else if (strcmp(command_list[i][j], ">") == 0) {
                    if (command_list[i].size()-2 == j){
                        std::cerr << "Invalid command.\n";
                    }
                    i_o_interpret(command_list[i][j+1], false);
                    command_list[i].erase(command_list[i].begin() + j);
                    command_list[i].erase(command_list[i].begin() + j);
                    j--;
                    j--;
                }
            }


            // Redirecting output for all commands except the last
            if(i != num_commands - 1){
                dup2(file_descriptors[1], 1);
            }
            close(file_descriptors[0]);
            close(file_descriptors[1]);
            int err = execvp(command_list[i][0], command_list[i].data());
            if (err<0){
                std::cerr << "The exec fails";
            }
            std::cerr<<EACCES;
        }
        else{
        //PARENT
        close(file_descriptors[1]); // Close write-end as it's not used

        in_fd = file_descriptors[0]; // Save the reading end of the pipe
        int status1;
        waitpid(cpid, &status1, 0);
        if (WIFEXITED(status1)) {
            int exit_status1 = WEXITSTATUS(status1);
            std::cout << command_list[i][0] << " exit status: " << exit_status1 << std::endl;
        }
        }
    }

    // The parent waits for all child processes to finish
    for(int i = 0; i < num_commands; i++){
        wait(NULL);
    }
}



void cleanup_args(std::vector<char*>& args) {
    for (char* arg : args) {
        delete[] arg;
    }
    args.clear();
}

string trim(const string &s) {
    auto start = s.begin();
    while (start != s.end() && isspace(*start)){
        start++;
    }
    auto end = s.end();
    while (end != start && isspace(*(end-1))){
        end--;
    }
    // if (*end == '|'){
    // std::cerr << "Invalid command.\n";
    // exit(0);
    // }
    string output = string(start,end);
    if(output.back() == '|'){
        std::cerr << "invalid command.\n";
        exit(0);
    }
    return output;
}

void echo(char **args){
    int i = 1;
    while (args[i]){
        std::cout << args[i] << (args[i + 1] ? " " : "\n");
        i++;
    }
}

int i_o_interpret(const char * fileName, bool input){
    if (input){
        int ID1 = open(fileName, O_RDONLY);
        if (!ID1){
            std::cerr << EACCES;
            //exit(255);
        }
        int temporary1 = dup2(ID1, STDIN_FILENO);
        int ID_old1 = close(ID1);
        if (ID_old1 !=0){
            std::cerr << EIO;
            //exit(255);
        }
        return temporary1; //error if this is less than 0
    }
    else{
        mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
        int ID = open(fileName, O_WRONLY | O_CREAT | O_TRUNC, mode);
        if (ID<0){
            std::cerr << EACCES;
            //exit(255);
        }

        int temporary = dup2(ID, STDOUT_FILENO);
        close(ID);
        return temporary;
    }
}

void parse_and_run_command(const std::string &command) {
    //bool isPipe = command.find('|')!=std::string::npos;
    //ensures a space before the pipe
    string commandTemp = command;
    bool isPipe = command.find(" | ")!= string::npos;
    if (isPipe) {
        if (!commandTemp.empty()) {
            commandTemp.resize(commandTemp.size() - 1);
        }
        bool isPipe_atEnd = commandTemp.find(" | ")!= string::npos;
        if (!isPipe_atEnd){
            std::cerr << "Invalid command.\n";
            exit(0);
        }

        vector<vector<char*>> commands_to_pipe = split_commands(command);
        pipeline(commands_to_pipe);
        int j = commands_to_pipe.size();
        for (int i = 0; i < j; ++i) {
            cleanup_args(commands_to_pipe[i]);
        }
    }
    else{
        if (command == "exit") {
            exit(0);
        }
        stringstream ss(command);
        string temp;
        vector<char *> command_vector;
        char *c;

        while (ss >> temp){
            c = new char[temp.size() + 1];
            strcpy(c, temp.c_str());
            command_vector.push_back(c);
        }

        command_vector.push_back(nullptr);

        // if (strcmp(command_vector[0], ">") == 0){
        // std::cerr << "Invalid command.\n";
        // } else if (strcmp(command_vector[0], "<") == 0){
        if (strcmp(command_vector[0], "<") == 0){
            std::cerr << "Invalid command.\n";
        }

        if (strcmp(command_vector[command_vector.size() - 2], ">") == 0){
            std::cerr << "Invalid command.\n";
        } 
        else if (strcmp(command_vector[command_vector.size() - 2], "<") == 0){
            std::cerr << "Invalid command.\n";
        }

        int child_pid = fork();

        if (child_pid < 0) {
            std::cerr << "Fork error.\n";
        }

        if (child_pid == 0) {
            bool isRedirect = false;
        for (size_t i = 0; i < command_vector.size() - 1; i++) {
            if (strcmp(command_vector[i], "<") == 0) {
                isRedirect = true;
                i_o_interpret(command_vector[i+1], true);
                command_vector.erase(command_vector.begin() + i);
                command_vector.erase(command_vector.begin() + i);
                i--;
                i--;
            } else if (strcmp(command_vector[i], ">") == 0) {
                isRedirect = true;
                i_o_interpret(command_vector[i+1], false);
                command_vector.erase(command_vector.begin() + i);
                command_vector.erase(command_vector.begin() + i);
                i--;
                i--;
            }
        }

        int err = execvp(command_vector[0], command_vector.data());
        if (err<0){
            //perror("error:");
            if(isRedirect){std::cerr << "invalid command";}
            else{std::cerr << "No such file or directory";}

        }
        //std::cerr << "No such file or directory\n";
        cleanup_args(command_vector);
        //exit(255);
        }

        else if (child_pid > 0) {
            int status;
            waitpid(child_pid, &status, 0);
            if (WIFEXITED(status)) {
                int exit_status = WEXITSTATUS(status);
                std::cout << command_vector[0] << " exit status: " << exit_status << std::endl;
            }
        }

        for (char* arg : command_vector) {
            delete[] arg;
        }
    }
}


int main(void) {
    std::string command;
    std::cout << "> ";
    while (std::getline(std::cin, command)) {
        command = trim(command);
        if (!command.empty()){
            parse_and_run_command(command);
        }
        std::cout << "> ";
    }
    return 0;
}
