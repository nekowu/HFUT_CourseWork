#include<stdlib.h>
#include"Mem.h"

int main(void) {
	
	int select = 0;
	int mem;
	while (select!=9){
		printf("\n"); 
		printf("**************�ֶδ洢ģ��******************\n" );
		printf("*** 1�������ڴ�         2����������      ***\n");
		printf("*** 3�����̵���         4���ͷ��ڴ�      ***\n");
		printf("*** 5��������Ϣ         6�������ڴ���Ϣ  ***\n");
		printf("*** 7���������ݵ�����   8�����ش�������  ***\n");
		printf("*** 9���˳�                              ***\n");
		printf("********************************************\n");
		printf("�����������س�:" );
		scanf("%d",&select);
		int pid = 0;
		int main_length = 0;
		int data_length = 0;
		struct Program *p;
		switch (select)
		{
		case 1:
			//	int mem;
			printf("������Ҫ�����ڴ��С��"); 
			scanf("%d",&mem);
			init(mem);//�����ڴ� 
			break; 
		case 2: 
			printf("������Ҫ�����Ľ���ID,   ����γ���,    ���ݶγ���\n" );
			scanf("%d%d%d",&pid,&main_length,&data_length);
			if(Is_Pid_Used(pid)==1) {
				p = CreateProgram(pid, main_length, data_length);
				p->next = pro_head;
				pro_head= p;
				p = NULL;
			}else {
				printf("�ý���ID�Ѿ���ʹ��!\n");
			}
			break;
		case 3:
			printf("������Ҫ����Ľ���ID��");
			scanf("%d",&pid);
			// ���÷����ڴ溯��
			AllocateMem(pid);
			break;
		case 4:
			printf("������Ҫ�ͷŵĽ���ID��");
			scanf("%d",&pid);
			RecycleMem(pid);
			break;
		case 5:
			display();
			break;
		case 6:
			printMemory();
			break;
		case 7:
		 	save_program_mes();
		 	//save_segtable_mes();
		 	break;
		case 8:
			load_program_mes();
			break;
		case 9:
			break;			
		default:
			printf("���������������");
			break;
		}
	} 
	return 0;

}
