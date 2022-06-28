#include<stdlib.h>
#include"Mem.h"

int main(void) {
	
	int select = 0;
	int mem;
	while (select!=9){
		printf("\n"); 
		printf("**************分段存储模型******************\n" );
		printf("*** 1、申请内存         2、创建进程      ***\n");
		printf("*** 3、进程调入         4、释放内存      ***\n");
		printf("*** 5、进程信息         6、可用内存信息  ***\n");
		printf("*** 7、保存数据到磁盘   8、加载磁盘数据  ***\n");
		printf("*** 9、退出                              ***\n");
		printf("********************************************\n");
		printf("请输入操作后回车:" );
		scanf("%d",&select);
		int pid = 0;
		int main_length = 0;
		int data_length = 0;
		struct Program *p;
		switch (select)
		{
		case 1:
			//	int mem;
			printf("请输入要申请内存大小："); 
			scanf("%d",&mem);
			init(mem);//申请内存 
			break; 
		case 2: 
			printf("请输入要创建的进程ID,   程序段长度,    数据段长度\n" );
			scanf("%d%d%d",&pid,&main_length,&data_length);
			if(Is_Pid_Used(pid)==1) {
				p = CreateProgram(pid, main_length, data_length);
				p->next = pro_head;
				pro_head= p;
				p = NULL;
			}else {
				printf("该进程ID已经被使用!\n");
			}
			break;
		case 3:
			printf("请输入要调入的进程ID：");
			scanf("%d",&pid);
			// 调用分配内存函数
			AllocateMem(pid);
			break;
		case 4:
			printf("请输入要释放的进程ID：");
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
			printf("输入错误重新输入");
			break;
		}
	} 
	return 0;

}
