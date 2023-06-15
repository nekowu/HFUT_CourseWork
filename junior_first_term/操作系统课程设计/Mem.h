#include<stdbool.h>
#include<stdio.h>

struct Program
{
	int pid; // ����id
	struct Program *next; // ��һ�����̵�id
	int main_seg_num;  //����κ� 
	int main_length; // ����γ�	
	int data_seg_num;// ���ݶκ� 
	int data_length;//���ݶγ� 
			
};

struct Program *pro_head; //����ͷ���

//�α�					  
struct Segtable
{
	int seg_num; // �κ�
	int seg_length; // �γ�
	int base_addr; // ��ַ
	struct Segtable *next; // ��һ����ָ��
};
struct Segtable *seg_table_head; // �α�ͷ

//�ڴ� 
struct Memory
{
	int addr;   // ʼַ
	int length; // ����
	struct Memory *next; // ��һ��
};

struct Memory *mem_head;

void init();//��ʼ�� 

// pid �Ƿ���Ч���Ƿ��ظ�
bool Is_Pid_Used(int pid);
// ��������
struct Program *CreateProgram(
	int pid, // pid
	int main_length, // main��
	int data_length // ���ݶ�
);


// �����ڴ�
void AllocateMem(int pid);
// ����α�
void AllocateSeg(struct Program *pro);
// �Ƿ���Է����ڴ�
bool Is_Allocate(int length1, int length2);
// ����α����ضκ�
int allocateSeg(int length);
// �����ڴ淵�ػ�ַ
int allocateMem(int length);
// ���ն� 
void RecycleSeg(int seg_num);
// �����ڴ�
void RecycleMem(int pid);
// �����ڴ�
void sort();
//���������Ϣ 
void save_program_mes(); 
// 
void save_segtable_mes();
//��ȡ�ڴ���Ϣ 
void load_program_mes();

void display(); // ��ʾ���̺Ͷα� 
void printProgram(); // ��ʾ������Ϣ
void printMemory();    // ��ʾ�����ڴ���Ϣ
void printSegment(); // ��ʾ�α���Ϣ


