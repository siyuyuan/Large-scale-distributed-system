# 引言
本书旨在成为使用Hadoop开发和运行软件的实用指南，Hadoop是Apache软件基金会主办的一个项目.
本章为大家介绍核心Hadoop，concEpts.它旨在为下一章做好准备，在这一章中，您将安装并运行Hadoop。

# 介绍Hadoop
Hadoop的核心是基于Java的MapReduce框架。 
但是，由于Hadoop平台的迅速采用，需要支持非Java用户社区。 Hadoop演变为具有以下增强功能和子项目，以支持该社区并将其范围扩展到企业中：
1. Hadoop Streaming:：使用Map Reduce启用任何命令行脚本。这使得UNIX脚本程序员、Python程序员等都可以使用Map Reduce来开发临时作业
2. Hadoop Hive： Hive Query语言与SQL语言十分相似，可以便于SQl程序员
3. Hadoop Pig：类似于Hive
4. Hadoop HBase: 前面的所有项目（包括MapReduce）都是批处理过程。
但是，在Hadoop中非常需要实时数据查找。 Hadoop没有本地密钥/值存储。 例如，考虑一个社交媒体网站，例如Facebook。 如果您想查找朋友的个人资料，则希望能够立即得到答案（而不是很久以后）。 这样的用例是开发HBase平台的动机。

在很长一段时间内，Hadoop仍然是一个用户提交作业的系统，这些作业运行在整个集群上。作业将在先进先出模式下执行。然而，这导致了这样一种情况：一项长期的、不那么重要的工作会占用资源，而不允许执行一项较小但更重要的工作。为了解决这个问题，为了解决此问题，在Hadoop中创建了更复杂的作业调度程序，例如Fair Scheduler和Capacity Scheduler。但是Hadoop1.x（在0.23版本之前）仍然存在可伸缩性限制。随着人们对这些问题的理解得到了进一步的了解，Hadoop工程师回到了图纸板上，重新评估了原始Hadoop设计背后的一些核心假设。 最终，这导致对核心Hadoop平台的重大设计大修。 Hadoop 2.x（来自Hadoop 0.23版）是此改革的结果。

本书将涵盖2.x版，并带有对1.x的适当引用。

# 介绍MapReduce Model
Hadoop支持MapReduce模型，该模型是Google引入的一种解决大型商用机器集群的千万亿级问题的方法。 该模型基于两个不同的步骤，这两个步骤都是针对应用程序定制和用户定义的：
1. Map：初始摄取和转换步骤，其中可以并行处理单个输入记录
2. Reduce：聚合或汇总步骤，其中所有关联记录必须由单个实体一起处理

Hadoop中的MapReduce的核心概念是可以将输入分为逻辑块，并且每个块可以由map任务进行初始处理。 这些单独的处理块的结果可以物理上划分为不同的集合，然后进行排序。 每个排序的块都传递给reduce任务。

Map任务可以在群集中的任何计算节点上运行，并且多个Map任务可以在群集中并行运行。 Map任务负责将输入记录转换为键/值对。 所有Map的输出将被分区，并对每个分区进行排序。 每个缩减任务将有一个分区。 然后，由reduce任务处理每个分区的排序键以及与这些键关联的值。 集群上可以并行运行多个reduce任务。

通常，应用程序开发人员仅向Hadoop框架提供四项items：读取输入记录并将其转换为每个记录一个键/值对的类，Mapper类，Reducer类以及一个将reduce方法输出的键/值对转换为输出记录的类。 让我们使用现在已成为MapReduce模型的“ Hello-World”（字数统计应用程序）来说明MapReduce的概念。

假设我们有大量的文本文档（非结构化）。我们可以对文本执行许多有趣的分析（例如，信息提取，基于内容的文档聚类，以及基于情感的文档分类）。 但是，大多数此类分析都是从获取文档语料库中每个单词的计数开始（文档集合通常称为语料库）。统计词频最朴素的办法就是创建字典遍历语料库。但是，主要的问题是数据的大小（毕竟，这本书是关于大数据的）。 当文档语料库为TB级时，可能需要数小时甚至几天才能在单个节点上完成该过程。 因此，当数据规模很大时，我们使用MapReduce解决该问题。 这是您会遇到的常见情况：您有一个非常简单的问题，根本无法在一台计算机上扩展。 您应该使用MapReduce。上述解决方案的MapReduce实现如下：
1. 预配大型计算机集群。 我们假设群集大小为50。
2. 每台计算机上都运行大量映射进程。 假设Map process将与文件一样多。假设有1000万个文件，将启动一千万个Map process。 在给定的时间，我们假设正在运行的Map process与CPU内核一样多。 给定一个双四核CPU机器，我们假设八个Mappers同时运行，因此每台机器负责运行200,000个Map进程。 因此，在处理期间，每台计算机上运行的8个Mappers共有25,000次迭代（每个迭代运行8个Mappers，每个内核运行一个）。
3. 每个Mapper处理一个文件，提取单词，并发出以下键/值对：<{WORD}，1>。 以下是Mapper输出的示例：
- <the，1>
- <the，1>
- <test，1>
4. 假设我们有一个Reducer
5.  Reducer接收具有以下格式的键/值对：<{WORD}，[1，.... 1]>。也就是说，Reducer接收到的键/值对是从任何Mappers发出的单词， Reducer输入键/值的示例如下：
- <the，[1,1,1，...，1]>
- <test，[1,1]>
6. Reducer只需将1加起来即可提供{WORD}的最终计数，并将结果作为以下键/值对发送到输出：<{WORD}，{COUNT OF WORD}>。 Reducer输出的示例如下：
- <the，1000101>
- <test，2>

在reduce阶段中接收键值列表的键是MapReduce中称为sort / shuffle阶段的阶段。映射器发出的所有键/值对均按Reducer中的键排序。如果分配了多个Reducer，则会将一个键的子集分配给每个Reducer。给定Reducer的键/值对按键排序，以确保与Reducer一起接收与一个键关联的所有值。

# Hadoop组成
在本节中，我们将开始深入研究Hadoop的各个组件。 我们将从Hadoop 1.x组件开始，最后讨论新的2.x组件。 Hadoop 1.x在较高级别上具有以下守护程序：
1. NameNode：维护HDFS中存储的每个文件的元数据。 元数据包括有关包含文件的块的信息以及它们在数据节点上的位置。 正如您将很快看到的，这是1.x的组件之一，成为大型集群的瓶颈。
2. Secondary NameNode：这不是backup NameNode。 它为NameNode执行一些内部管理功能。
3. DataNode：将文件的实际块存储在HDFS自身的本地磁盘上。
4. JobTracker：主组件之一，它负责管理作业的整体执行。 它执行的功能包括将子任务（单独的Mapper和Reducer）调度到各个节点，跟踪每个任务和节点的运行状况，甚至重新调度失败的任务。 正如我们将很快演示的，就像NameNode一样，在将Hadoop扩展到超大型集群时，Job Tracker成为瓶颈。
5. TaskTracker：在单个DataNode上运行，并负责启动和管理单个Map / Reduce任务。 与JobTracker通信。

Hadoop 1.x集群具有两种类型的节点：master nodes和slave nodes。 master nodes负责运行以下守护程序：
- NameNode
- Secondary NameNode
- JobTracker

slave nodes分布在整个群集中，并运行以下守护程序：
- DataNode
- TaskTracker

尽管每个主守护程序只有一个实例在整个集群上运行，但是DataNode和TaskTracker却有多个实例。 在较小的集群或开发/测试集群上，通常三个主守护程序都在同一台计算机上运行。 但是，对于生产系统或大型集群，将它们放在单独的节点上更为谨慎。

# Hadoop Distributed File System (HDFS)
HDFS旨在支持使用非常大文件的应用程序。这样的应用程序写一次数据，并多次读取相同的数据。HDFS是以下几个守护进程共同作用的结果：
- NameNode
- Secondary NameNode
- DataNode
尽管每个主守护程序只有一个实例在整个集群上运行，但是DataNode和TaskTracker却有多个实例。 在较小的集群或开发/测试集群上，通常三个主守护程序都在同一台计算机上运行。 但是，对于生产系统或大型集群，将它们放在单独的节点上更为谨慎。
