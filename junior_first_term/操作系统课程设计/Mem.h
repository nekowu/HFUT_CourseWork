#include<stdbool.h>
#include<stdio.h>

struct Program
{
	int pid; // 进程id
	struct Program *next; // 下一个进程的id
	int main_seg_num;  //程序段号 
	int main_length; // 程序段长	
	int data_seg_num;// 数据段号 
	int data_length;//数据段长 
			
};

struct Program *pro_head; //进程头结点

//段表					  
struct Segtable
{
	int seg_num; // 段号
	int seg_length; // 段长
	int base_addr; // 基址
	struct Segtable *next; // 下一个段指针
};
struct Segtable *seg_table_head; // 段表头

//内存 
struct Memory
{
	int addr;   // 始址
	int length; // 长度
	struct Memory *next; // 下一个
};

struct Memory *mem_head;

void init();//初始化 

// pid 是否有效，是否重复
bool Is_Pid_Used(int pid);
// 创建进程
struct Program *CreateProgram(
	int pid, // pid
	int main_length, // main段
	int data_length // 数据段
);


// 分配内存
void AllocateMem(int pid);
// 分配段表
void AllocateSeg(struct Program *pro);
// 是否可以分配内存
bool Is_Allocate(int length1, int length2);
// 分配段表并返回段号
int allocateSeg(int length);
// 分配内存返回基址
int allocateMem(int length);
// 回收段 
void RecycleSeg(int seg_num);
// 回收内存
void RecycleMem(int pid);
// 整理内存
void sort();
//保存程序信息 
void save_program_mes(); 
// 
void save_segtable_mes();
//读取内存信息 
void load_program_mes();

void display(); // 显示进程和段表 
void printProgram(); // 显示进程信息
void printMemory();    // 显示空闲内存信息
void printSegment(); // 显示段表信息


