#include"Mem.h"
#include<malloc.h>
#include <stdlib.h>
//int mem=1024;
int current_seg_num=0;
// �����ڴ��ʼ��������1 
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
//�������� 
struct Program *CreateProgram(int pid, int main_length, int data_length) {
	struct Program *newPro;
	newPro = (struct Program*)malloc (sizeof(struct Program));
	//newPro = new program;
	newPro->pid = pid;
	newPro->main_length = main_length;
	newPro->main_seg_num = -1; // ��ʼ��
	newPro->data_length = data_length;
	newPro->data_seg_num = -1; // ��ʼ��
	newPro->next = NULL;
	return newPro;
}

// �����ڴ�
void AllocateMem(int pid) {
	struct Program *index;
	index = pro_head;
	if (index != NULL) {
		for (; index != NULL; index = index->next) {
			if (index->pid == pid) {
				if (index->main_seg_num == -1) {
					// �����
					AllocateSeg(index);
				}
				else {
					printf("�ѱ�����\n");
				}
			}
			//else{
			//printf("�޴˽���\n");
			//break;
			//} 
		}
	}
}

// ���̷����
void AllocateSeg(struct Program *pro) {
	struct Program *tmp;
	tmp = pro;
	int main_length = tmp->main_length;
	int data_length = tmp->data_length;
	// �жϿ��Է���
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
		printf("�ڴ治���޷�����\n");
	}
}
// �ɷ���
bool Is_Allocate(int length1, int length2) {
	bool flag = false;
	bool alloc1 = false; // �������Σ���ʼ����־false 
	bool alloc2 = false; // �������ݶΣ���ʼ����־false  
	struct Memory *index;
	index = mem_head;
	int selected_addr = -1; // �Ѿ�ѡ���˵Ľڵ�
	for (; index != NULL; index = index->next) {
		// �����ڴ�鳤�ȴ��ڳ���γ��� 
		if (index->length >= length1) {
			alloc1 = true;//���� 
			int sub = 0;
			sub = index->length - length1;
			//���������Σ������ڴ��ʣ�೤�Ȼ��������ݶ� 
			if (sub >= length2 && !alloc2) {
				alloc2 = true;// �������ݶ�
				break; // �˳�
			}
			else {
				selected_addr = index->addr; // �õ�ַ�Ѿ������������� 
				break; // �˳�
			}
		}
	}
	//�����ڴ��������ݶ� 
	if (!alloc2) { 
		index = mem_head;
		for (; index != NULL; index = index->next) {
			if (index->length >= length2 && index->addr != selected_addr) {
				// �����ڴ��������ݶ���û�б������ռ��
				alloc2 = true;
				break;
			}
		}
	}

	//������Գɹ� 
	if (alloc1 && alloc2) {
		flag = true;
	}
	return flag;
}

// ����α�
int allocateSeg(int length) {
	struct Segtable*item;
	item = (struct Segtable*)malloc(sizeof(struct Segtable));
	item->seg_length = length;//�γ� 
	//�����ڴ�
	item->base_addr = allocateMem(length);
	item->seg_num = current_seg_num;
	item->next = NULL;
	int renum = -1; // ����ֵ
	current_seg_num += 1; // �κż�һ
						  
	struct Segtable*p;// ����α�
	bool flag = false; // �Ƿ������
	p = seg_table_head;
	if (p == NULL) {	// δ����
		seg_table_head = item;//���� 
		renum = item->seg_num;
	}
	else { // ����β��
		   // Ѱ��ֵΪ-1�Ľ��з���
		for (; p != NULL; p = p->next) {
			if (p->seg_length == -1) {
				// ����û��ʹ��
				renum = p->seg_num;
				p->base_addr = item->base_addr;
				p->seg_length = item->seg_length;
				current_seg_num -= 1;
				free(item); // ɾ���ýڵ�
				flag = true; // �Ѿ�����öα�
				break;
			}
		}
		// ���������δ����,����β�����һ���ڵ�
		p = seg_table_head;
		if (!flag) {
			// �ҵ�β��
			if (p->next == NULL) {
				p->next = item; // ����β��
				renum = item->seg_num;
			}
			else {
				// ��λ��β��
				for (; p->next != NULL; p = p->next) { 
				continue; 
				}
				p->next = item;
				renum = item->seg_num;
			}
		}
	}
	return renum; // ���ضα�κ�
}

//�����ڴ�
int allocateMem(int length) {
	// ���������ڴ�飬�ҵ���һ��>=�����䳤�ȵ�
	struct Memory*idle, *pre;
	idle = mem_head;
	pre = mem_head; // ǰ��ָ��
	int base_addr; // ��ʼ��ַ
				   // ������ʼ 
	for (; (idle->length < length) && idle != NULL; idle = idle->next) {
		pre = idle; // ����ǰ��ָ��
	}
	if (idle == NULL) {
		//���ڴ������ 
		printf( "�޷�����\n");
	}
	else {
		//�ɷ������ 
		if (idle->length == length) {
			//ǡ�÷��룬ɾ���ÿ��п飬�ϲ������ڴ� 
			pre->next = idle->next;
			base_addr = idle->length;
			free(idle); // ɾ���ڵ�
		}
		else {
			// �޷��������ڴ�� 
			base_addr = idle->addr;
			idle->addr = base_addr + length;
			idle->length = idle->length - length; // ���¿��п�Ĵ�С 
		}
	}
	return base_addr; // ���ػ�ַ
}

// �����ڴ�
void RecycleMem(int pid) {
	struct Program *index;
	index = pro_head;
	for (; index != NULL; index = index->next) {
		// �ҵ����̵Ľڵ�
		if (index->pid == pid) {
			//�ҵ�����Σ����ݶζκ� 
			int main_seg_num = index->main_seg_num;
			int data_seg_num = index->data_seg_num;
			if (main_seg_num != -1 && data_seg_num != -1) {
				// ���ð��κŻ����ڴ�
				RecycleSeg(main_seg_num); // ���նκŻ����ڴ�
				index->main_seg_num = -1; // �ָ��ɳ�ʼ��
				RecycleSeg(data_seg_num); // ���նκŻ����ڴ�
				index->data_seg_num = -1; // �ָ��ɳ�ʼ��
			}
		}
	}
}

// �κŻ����ڴ�
void RecycleSeg(int seg_num) {
	struct Segtable*item;
	item = seg_table_head;
	// ���ݶκ��ҵ��ö� 
	for (; item != NULL; item = item->next) {
		if (item->seg_num == seg_num) {
			break;
		}
	}
	//�α��Ⱥͻ���ַ�ó�ʼ��
	int base_addr;
	int seg_length;
	if (item != NULL) {
		base_addr = item->base_addr;
		seg_length = item->seg_length;
		item->base_addr = -1;
		item->seg_length = -1;
		// ���п� 
		struct Memory *idle;
		idle = (struct Memory*)malloc(sizeof(struct Memory));
		idle->addr = base_addr;
		idle->length = seg_length;
		// ����
		struct Memory *index;
		index = mem_head;
		if (base_addr < index->addr) {
			//��ͷ������ 
			idle->next = index;
			mem_head = idle;
		}else {
			for (; index != NULL; index = index->next) {
				if (index->next == NULL) {
					index->next = idle;
					// ��β������ 
				}else {
					int pre_addr = index->addr + index->length;
					int next_addr = index->next->addr;
					if (base_addr >= pre_addr && base_addr <= next_addr) {
						// ���м�ֵ�������м�
						idle->next = index->next;
						index->next = idle;
						break;
					}
				}
			}
		}

	}
	// ���������
	sort();
}

// �������������
void sort() {
	// ����������ڵĿ���������β��� ���ϲ� 
	struct Memory *index;
	index = mem_head;
	while (index != NULL && index->next != NULL) {
		// ǰһ��β��ַ
		int tear_addr = index->addr + index->length;
		// ��һ���׵�ַ
		int head_addr = index->next->addr;
		if (tear_addr == head_addr) {
			struct Memory *tmp;
			tmp = index->next;
			// ���Ⱥϲ� 
			index->length = index->length + tmp->length;
			// ָ��ת��
			index->next = tmp->next; // �������ϲ��Ľڵ�					
			free(tmp);	 // ɾ���ڵ�
			continue;
		}
		// ������һ��
		index = index->next;
	}
	index = NULL;// ���
}
void save_program_mes()
{
	FILE *fp=fopen("program_data.txt","w");
    if(fp==NULL)
    {
        printf("�޷���program_data.txt! " );
        exit(0);
    }
    else{
    	printf("���ڱ���program_data.txt...\n");
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
	//printf("����ɹ�\n");
	
} 
void save_segtable_mes(){
	FILE *fp=fopen("segtable_data.txt","w");
    if(fp==NULL)
    {
        printf("�޷���segtable_data.txt! " );
        exit(0);
    }
    else{
    	printf("���ڱ���segtable_data.txt...\n");
	}
    struct Segtable*item;
	item = seg_table_head; // 
	while(item){
	for (; item != NULL; item = item->next) {
			fprintf(fp,"%d,%d,%d\n", (item->seg_num), (item->base_addr), (item->seg_length));
			//printf("%d,%d,%d\n", (item->seg_num), (item->base_addr), (item->seg_length));
	}	
	}	
	printf("����ɹ�\n"); 
	fclose(fp);


}
void save_memory_mes()
{
		FILE *fp=fopen("memory_data.txt","w");
    if(fp==NULL)
    {
        printf("�޷���memory_data.txt! " );
        exit(0);
    }
    else{
    	printf("���ڱ���memory_data.txt...\n");
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
        printf("�޷���program_data.txt! " );
        exit(0);
    }
    else
	{
    	printf("���ڶ�ȡprogram_data.txt...\n");
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
	printf("��ȡ�ɹ���\n"); 	
}

void display() {
	
	printf("******************************������Ϣ***********************************\n");
	printProgram(); // 
	printf("*************************************************************************\n");
	printf("******************************�α���Ϣ***********************************\n");
	printSegment();
	printf("*************************************************************************\n") ;

}

// ��ʾӦ��������Ϣ
void printProgram() {
	struct Program *t;
	t = pro_head;
	if (t == NULL) {
		printf("�޽���\n");
	}
	else {
		printf("���̺�        ����γ�        ����κ�         ���ݶγ�         ���ݶκ�\n");
		for (; t != NULL; t = t->next) {
		printf(" %d               %d               %d                %d               %d\n",(t->pid),(t->main_length),(t->main_seg_num),(t->data_length),(t->data_seg_num));	
		}
	}
}

// ��ʾ�α���Ϣ
void printSegment() {
	struct Segtable*item;
	item = seg_table_head; // 
	if (item == NULL) {
		printf( "δ�����\n");
	}
	else {
		printf("�κ�          ��ַ             �γ�\n");
		for (; item != NULL; item = item->next) {
			printf("%d              %d                 %d\n", (item->seg_num), (item->base_addr), (item->seg_length));
		}
	}
}

// ��ʾ������Ϣ
void printMemory() {
	struct Memory *mem;
	mem = mem_head;
	printf("********�����ڴ���Ϣ**********\n");
	printf("�ڴ�ʼַ            ���ó���\n");
	while (mem != NULL)
	{
		printf("%d                     %d\n", (mem->addr), (mem->length));
		mem = mem->next;
	}
	printf("******************************\n");
}
