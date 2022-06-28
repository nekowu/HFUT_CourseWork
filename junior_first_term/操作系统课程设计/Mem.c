#include"Mem.h"
#include<malloc.h>
#include <stdlib.h>
//int mem=1024;
int current_seg_num=0;
// 申请内存初始化，功能1 
void init(int mem) {
	struct Memory *idle;
	idle=(struct Memory*)malloc(sizeof(struct Memory)); 
	//idle = new Idle_section;
	idle->addr = 0;
	idle->length = mem;
	idle->next = NULL;
	mem_head = idle;
	seg_table_head = NULL;	
	pro_head= NULL;
}


bool Is_Pid_Used(int pid) {
	struct Program *index;
	bool flag = true;
	index = pro_head;
	if (index != NULL) {
		for (; index!= NULL; index=index->next) {
			if (pid == index->pid) {
				flag = false;
			}
		}
	}
	return flag;
}
//创建进程 
struct Program *CreateProgram(int pid, int main_length, int data_length) {
	struct Program *newPro;
	newPro = (struct Program*)malloc (sizeof(struct Program));
	//newPro = new program;
	newPro->pid = pid;
	newPro->main_length = main_length;
	newPro->main_seg_num = -1; // 初始化
	newPro->data_length = data_length;
	newPro->data_seg_num = -1; // 初始化
	newPro->next = NULL;
	return newPro;
}

// 分配内存
void AllocateMem(int pid) {
	struct Program *index;
	index = pro_head;
	if (index != NULL) {
		for (; index != NULL; index = index->next) {
			if (index->pid == pid) {
				if (index->main_seg_num == -1) {
					// 分配段
					AllocateSeg(index);
				}
				else {
					printf("已被调入\n");
				}
			}
			//else{
			//printf("无此进程\n");
			//break;
			//} 
		}
	}
}

// 进程分配段
void AllocateSeg(struct Program *pro) {
	struct Program *tmp;
	tmp = pro;
	int main_length = tmp->main_length;
	int data_length = tmp->data_length;
	// 判断可以分配
	if (Is_Allocate(main_length, data_length)) {
		if (main_length > 0) {
			int main_num = allocateSeg(main_length);
			tmp->main_seg_num = main_num;
		}

		if (data_length > 0) {
			int data_num = allocateSeg(data_length);
			tmp->data_seg_num = data_num;
		}

	}
	else {
		printf("内存不足无法分配\n");
	}
}
// 可分配
bool Is_Allocate(int length1, int length2) {
	bool flag = false;
	bool alloc1 = false; // 分配程序段，初始化标志false 
	bool alloc2 = false; // 分配数据段，初始化标志false  
	struct Memory *index;
	index = mem_head;
	int selected_addr = -1; // 已经选择了的节点
	for (; index != NULL; index = index->next) {
		// 可用内存块长度大于程序段长度 
		if (index->length >= length1) {
			alloc1 = true;//分配 
			int sub = 0;
			sub = index->length - length1;
			//分配完程序段，可用内存块剩余长度还大于数据段 
			if (sub >= length2 && !alloc2) {
				alloc2 = true;// 分配数据段
				break; // 退出
			}
			else {
				selected_addr = index->addr; // 该地址已经分配给程序段了 
				break; // 退出
			}
		}
	}
	//另找内存块分配数据段 
	if (!alloc2) { 
		index = mem_head;
		for (; index != NULL; index = index->next) {
			if (index->length >= length2 && index->addr != selected_addr) {
				// 空闲内存块大于数据段且没有被程序段占用
				alloc2 = true;
				break;
			}
		}
	}

	//分配测试成功 
	if (alloc1 && alloc2) {
		flag = true;
	}
	return flag;
}

// 分配段表
int allocateSeg(int length) {
	struct Segtable*item;
	item = (struct Segtable*)malloc(sizeof(struct Segtable));
	item->seg_length = length;//段长 
	//分配内存
	item->base_addr = allocateMem(length);
	item->seg_num = current_seg_num;
	item->next = NULL;
	int renum = -1; // 返回值
	current_seg_num += 1; // 段号加一
						  
	struct Segtable*p;// 加入段表
	bool flag = false; // 是否分配标记
	p = seg_table_head;
	if (p == NULL) {	// 未分配
		seg_table_head = item;//分配 
		renum = item->seg_num;
	}
	else { // 插入尾部
		   // 寻找值为-1的进行分配
		for (; p != NULL; p = p->next) {
			if (p->seg_length == -1) {
				// 该条没有使用
				renum = p->seg_num;
				p->base_addr = item->base_addr;
				p->seg_length = item->seg_length;
				current_seg_num -= 1;
				free(item); // 删除该节点
				flag = true; // 已经分配好段表
				break;
			}
		}
		// 如果上述都未分配,则在尾部添加一个节点
		p = seg_table_head;
		if (!flag) {
			// 找到尾部
			if (p->next == NULL) {
				p->next = item; // 插入尾部
				renum = item->seg_num;
			}
			else {
				// 定位到尾部
				for (; p->next != NULL; p = p->next) { 
				continue; 
				}
				p->next = item;
				renum = item->seg_num;
			}
		}
	}
	return renum; // 返回段表段号
}

//分配内存
int allocateMem(int length) {
	// 遍历空闲内存块，找到第一个>=待分配长度的
	struct Memory*idle, *pre;
	idle = mem_head;
	pre = mem_head; // 前驱指针
	int base_addr; // 起始地址
				   // 遍历开始 
	for (; (idle->length < length) && idle != NULL; idle = idle->next) {
		pre = idle; // 保留前驱指针
	}
	if (idle == NULL) {
		//到内存最后了 
		printf( "无法分配\n");
	}
	else {
		//可分配情况 
		if (idle->length == length) {
			//恰好放入，删除该空闲块，合并已用内存 
			pre->next = idle->next;
			base_addr = idle->length;
			free(idle); // 删除节点
		}
		else {
			// 无法填满该内存块 
			base_addr = idle->addr;
			idle->addr = base_addr + length;
			idle->length = idle->length - length; // 更新空闲块的大小 
		}
	}
	return base_addr; // 返回基址
}

// 回收内存
void RecycleMem(int pid) {
	struct Program *index;
	index = pro_head;
	for (; index != NULL; index = index->next) {
		// 找到进程的节点
		if (index->pid == pid) {
			//找到程序段，数据段段号 
			int main_seg_num = index->main_seg_num;
			int data_seg_num = index->data_seg_num;
			if (main_seg_num != -1 && data_seg_num != -1) {
				// 调用按段号回收内存
				RecycleSeg(main_seg_num); // 按照段号回收内存
				index->main_seg_num = -1; // 恢复成初始化
				RecycleSeg(data_seg_num); // 按照段号回收内存
				index->data_seg_num = -1; // 恢复成初始化
			}
		}
	}
}

// 段号回收内存
void RecycleSeg(int seg_num) {
	struct Segtable*item;
	item = seg_table_head;
	// 根据段号找到该段 
	for (; item != NULL; item = item->next) {
		if (item->seg_num == seg_num) {
			break;
		}
	}
	//段表长度和基地址置初始化
	int base_addr;
	int seg_length;
	if (item != NULL) {
		base_addr = item->base_addr;
		seg_length = item->seg_length;
		item->base_addr = -1;
		item->seg_length = -1;
		// 空闲块 
		struct Memory *idle;
		idle = (struct Memory*)malloc(sizeof(struct Memory));
		idle->addr = base_addr;
		idle->length = seg_length;
		// 插入
		struct Memory *index;
		index = mem_head;
		if (base_addr < index->addr) {
			//在头部插入 
			idle->next = index;
			mem_head = idle;
		}else {
			for (; index != NULL; index = index->next) {
				if (index->next == NULL) {
					index->next = idle;
					// 在尾部插入 
				}else {
					int pre_addr = index->addr + index->length;
					int next_addr = index->next->addr;
					if (base_addr >= pre_addr && base_addr <= next_addr) {
						// 找中间值，插入中间
						idle->next = index->next;
						index->next = idle;
						break;
					}
				}
			}
		}

	}
	// 整理空闲区
	sort();
}

// 整理空闲区函数
void sort() {
	// 如果两个相邻的空闲区，首尾相接 ，合并 
	struct Memory *index;
	index = mem_head;
	while (index != NULL && index->next != NULL) {
		// 前一块尾地址
		int tear_addr = index->addr + index->length;
		// 后一块首地址
		int head_addr = index->next->addr;
		if (tear_addr == head_addr) {
			struct Memory *tmp;
			tmp = index->next;
			// 长度合并 
			index->length = index->length + tmp->length;
			// 指针转向
			index->next = tmp->next; // 跳过被合并的节点					
			free(tmp);	 // 删除节点
			continue;
		}
		// 连接下一个
		index = index->next;
	}
	index = NULL;// 清空
}
void save_program_mes()
{
	FILE *fp=fopen("program_data.txt","w");
    if(fp==NULL)
    {
        printf("无法打开program_data.txt! " );
        exit(0);
    }
    else{
    	printf("正在保存program_data.txt...\n");
	}
    struct Program *t;
	t = pro_head;
	while(t){
	
	for (; t != NULL; t = t->next) {
		fprintf(fp,"%d,%d,%d,%d,%d\n",(t->pid),(t->main_length),(t->main_seg_num),(t->data_length),(t->data_seg_num));
		//fprintf(fp,"%d,%d,%d\n",(t->pid),(t->main_length),(t->data_length));
	}
	}	
	fclose(fp);
	//printf("保存成功\n");
	
} 
void save_segtable_mes(){
	FILE *fp=fopen("segtable_data.txt","w");
    if(fp==NULL)
    {
        printf("无法打开segtable_data.txt! " );
        exit(0);
    }
    else{
    	printf("正在保存segtable_data.txt...\n");
	}
    struct Segtable*item;
	item = seg_table_head; // 
	while(item){
	for (; item != NULL; item = item->next) {
			fprintf(fp,"%d,%d,%d\n", (item->seg_num), (item->base_addr), (item->seg_length));
			//printf("%d,%d,%d\n", (item->seg_num), (item->base_addr), (item->seg_length));
	}	
	}	
	printf("保存成功\n"); 
	fclose(fp);


}
void save_memory_mes()
{
		FILE *fp=fopen("memory_data.txt","w");
    if(fp==NULL)
    {
        printf("无法打开memory_data.txt! " );
        exit(0);
    }
    else{
    	printf("正在保存memory_data.txt...\n");
	}
   struct Memory *idle;
	idle = mem_head;
	while(idle){
	fprintf(fp,"%d,%d\n", (idle->addr), (idle->length));
		
		idle = idle->next;
	} 
	fclose(fp);
}
void load_program_mes(){
	FILE *fp = fopen("program_data.txt","r");
	if(fp==NULL)
    {
        printf("无法打开program_data.txt! " );
        exit(0);
    }
    else
	{
    	printf("正在读取program_data.txt...\n");
	}
	
	int i=0,j; 
	char str;
	int arr[100000];
	while(fscanf(fp,"%c",&str)!=EOF)   
 	{
 	   if((str!=',')&&(str!='\n')){
 	   	arr[i]=(int)(str-'0');
				//printf("%d\n",arr[i]); 
				i++;
		}  
	}
/*
 	int m=0;
	 for(m=0;m<i;m++){
	 	printf("%d\n",arr[m]);
	 }
*/			
	struct Program *p;
	for(j=0;j<i;j+=5){
	//	printf("%d\n",arr[j]);
		p = CreateProgram(arr[j], arr[j+1],arr[j+3]);
		p->next = pro_head;
		pro_head = p;
		p = NULL;
	}

    fclose(fp);
	printf("读取成功！\n"); 	
}

void display() {
	
	printf("******************************进程信息***********************************\n");
	printProgram(); // 
	printf("*************************************************************************\n");
	printf("******************************段表信息***********************************\n");
	printSegment();
	printf("*************************************************************************\n") ;

}

// 显示应用链表信息
void printProgram() {
	struct Program *t;
	t = pro_head;
	if (t == NULL) {
		printf("无进程\n");
	}
	else {
		printf("进程号        程序段长        程序段号         数据段长         数据段号\n");
		for (; t != NULL; t = t->next) {
		printf(" %d               %d               %d                %d               %d\n",(t->pid),(t->main_length),(t->main_seg_num),(t->data_length),(t->data_seg_num));	
		}
	}
}

// 显示段表信息
void printSegment() {
	struct Segtable*item;
	item = seg_table_head; // 
	if (item == NULL) {
		printf( "未分配段\n");
	}
	else {
		printf("段号          基址             段长\n");
		for (; item != NULL; item = item->next) {
			printf("%d              %d                 %d\n", (item->seg_num), (item->base_addr), (item->seg_length));
		}
	}
}

// 显示空闲信息
void printMemory() {
	struct Memory *mem;
	mem = mem_head;
	printf("********可用内存信息**********\n");
	printf("内存始址            可用长度\n");
	while (mem != NULL)
	{
		printf("%d                     %d\n", (mem->addr), (mem->length));
		mem = mem->next;
	}
	printf("******************************\n");
}
