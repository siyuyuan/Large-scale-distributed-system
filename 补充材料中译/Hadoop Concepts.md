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
HDFS具有主/从体系结构。 NameNode是主节点，DataNode是从节点。 通常，DataNode守护程序在每个从属节点上运行。 它管理附加到每个DataNode的存储。 HDFS公开了文件系统名称空间，并允许将数据存储在节点群集中，同时为用户提供文件系统的单个系统视图。 NameNode负责管理文件的元数据。

## Block Storage Nature of Hadoop Files
首先，我们应该了解文件如何物理存储在群集中。在Hadoop中，每个文件都分为多个块。典型的块大小为64 MB，但配置32 MB或128 MB的块大小并非非常规。可以在HDFS中为每个文件配置块大小。如果文件不是块大小的精确倍数，则不会浪费空间，并且最后一个块小于总块大小。一个大文件将分为多个块，每个块都存储在一个DataNode上。它还被复制以确保不会出现故障。 Hadoop中的默认复制因子为3。支持机架的Hadoop系统在本地机架中的一个节点上存储一个块（假设Hadoop客户端在DataNode之一上运行；如果没有，则随机选择机架）。第二个副本放置在不同远程机架的节点上，最后一个节点放置在同一远程机架的节点上。通过在单独的网络拓扑文件中配置机架到节点的域名系统（DNS）名称映射，可以使Hadoop系统了解机架，该路径通过Hadoop配置文件进行引用。

为什么不将所有三个副本都放在不同的机架上呢？ 毕竟，这只会增加冗余。 这将进一步确保防止机架故障以及提高机架吞吐量。 但是，机架故障超过节点故障的可能性要小得多，并且尝试将副本保存到多个机架只会降低写入性能。 因此，需要进行权衡以将两个副本保存到同一远程机架上的节点，以换取更高的性能。 由性能约束引起的这种微妙的设计决策在Hadoop系统中很常见。
## File Metadata and NameNode
当客户端请求文件或决定将文件存储在HDFS中时，它需要知道要访问哪些DataNode。有了这些信息，客户端就可以直接写入各个DataNode。维护此元数据的责任在于NameNode。NameNode公开了文件系统名称空间，并允许将数据存储在节点群集中，同时允许用户查看文件系统的单个系统视图。 HDFS公开了文件系统的分层视图，其中文件存储在目录中，并且目录可以嵌套。 NameNode负责管理文件和目录的元数据。

NameNode管理所有操作，例如文件/目录的打开，关闭，重命名，移动等。 DataNode负责提供实际的文件数据。这是一个重要的区别！当客户端请求或发送数据时，数据实际上不会通过NameNode。这将是巨大的瓶颈。相反，客户端仅从NameNode获取有关文件的元数据，并直接从节点获取文件块。

元数据（Metadata），又称中介数据、中继数据，为描述数据的数据（data about data），主要是描述数据属性（property）的信息，用来支持如指示存储位置、历史数据、资源查找、文件记录等功能。元数据算是一种电子式目录，为了达到编制目录的目的，必须在描述并收藏数据的内容或特色，进而达成协助数据检索的目的。

NameNode存储的一些元数据包括：
- 文件/目录名称及其相对于父目录的位置。
- 文件和目录的ownership 和 permissions。
- 各个块的文件名。每个块都作为文件存储在文件的本地文件系统中。
Hadoop系统管理员可以配置的目录中的DataNode。我们需要注意的是，NameNode不会存储每个块的位置（DataNode标识）。在群集启动时从每个DataNode获取此信息。 NameNode仅维护有关组成HDFS的文件的块（数据节点上每个块的文件名）的信息。元数据存储在磁盘上，但在集群操作期间为了快速访问而加载到内存中。这方面对于Hadoop的快速运行至关重要，但同时也导致了Hadoop 2.x的主要瓶颈之一，每个元数据消耗约200字节的RAM。考虑一个1GB的文件，块大小为64 MB。这样的文件需要16 x 3（包括副本）= 48个存储块。现在考虑1,000个文件，每个文件1MB。该文件系统需要1000 x 3 = 3,000块存储。 （每个块只有1 MB大，但是不能在一个块中存储多个文件）。因此，这将导致NameNode上更多的内存使用情况。该示例还应用于解释为什么Hadoop系统偏爱大文件而不是小文件，因为大量的小文件只会使NameNode不堪重负。

包含元数据的NameNode文件为fsimage。系统操作期间对元数据的任何更改都存储在内存中，并保存到另一个称为edits的文件中。Secondary NameNode会定期将edits文件与fsimage文件合并。这些文件不包含实际数据,实际数据存储在运行DataNode守护程序的从属节点中的各个块上。如前所述，这些块只是从属节点上的文件。该块仅存储原始内容，不存储元数据。 因此，丢失NameNode元数据会使整个系统无法使用。 NameNode元数据使客户端能够理解从属节点上的原始存储块。DataNode守护程序会定期将心跳消息发送到NameNode。 这使NameNode可以了解每个DataNode的运行状况，而不会将任何客户端请求定向到发生故障的节点。

## Mechanics of an HDFS Write
HDFS写入操作与文件创建有关。我们将默认复制因子设为3。客户端将文件写入HDFS的步骤如下：
1. 在联系NameNode之前，客户端开始将文件内容流式传输到其本地文件系统中的临时文件
2. 当文件数据大小达到块大小时，客户端联系NameNode。
3. 现在，NameNode在HDFS文件系统层次结构中创建一个文件，并将数据块标识符和DataNodes的位置通知客户端。 此DataNodes列表还包含复制节点的列表。
4. 客户端使用上一步中的信息将临时文件刷新到从NameNode接收到的数据块位置（第一个DataNode）。 这导致在DataNode的本地存储上创建实际文件。
5. 关闭文件（客户端看到的HDFS文件）后，NameNode提交该文件，并且该文件在系统中变得可见。 如果NameNode在提交之前关闭，则该文件将丢失。

步骤4应该引起更多注意。 该步骤中的刷新过程操作如下：
1. 第一个DataNode以较小的数据包（通常为4 KB）从客户端接收数据。尽管此部分正在写入第一个DataNode上的磁盘，但它开始将其流式传输到第二个DataNode。
2. 第二个DataNode开始将流数据块写入其自己的磁盘，同时开始将数据块的数据包流向第三个DataNode。
3. 现在，第三个DataNode将数据写入其自己的磁盘。因此，数据以流水线方式通过DataNode写入和复制。
4. 确认数据包从每个DataNode发送回管道中的前一个数据包。第一个DataNode最终将确认发送到客户端节点。
5. 当客户端收到一个数据块的确认信息时，该数据块被假定为被持久化到所有节点，并将最后的确认信息发送给NameNode。
6. 如果管道中的任何DataNode发生故障，则管道将关闭。数据仍将被写入剩余的DataNodes，使NameNode知道文件未完全复制，并采取措施在良好的DataNode上重新复制数据，以确保足够的复制级别。
7. 每个块还计算校验和，校验和用于验证块的完整性。这些校验和存储在HDFS中的一个单独的隐藏文件中，用于在读取块数据时验证块数据的完整性。

## Mechanics of an HDFS Read
现在我们将讨论如何从HDFS读取文件。以下步骤使客户端可以读取文件：
1. 客户端联系NameNode，该NameNode返回块列表及其位置（包括副本位置）。
2. 客户端通过联系DataNode直接启动读取块。 如果DataNode失败，则客户端与托管副本的DataNode联系。
3. 读取块时，将计算校验和并将其与文件写入时计算的校验和进行比较。 如果校验和失败，则从副本中检索该块。

## Mechanics of an HDFS Delete
要从HDFS删除文件，请按照下列步骤操作：
1. NameNode仅重命名文件路径以指示文件已移至回收站。请注意，此处唯一发生的操作是链接到重命名文件路径的元数据更新操作。这是一个非常快的过程。该文件在回收站中保留了预定的时间间隔（当前设置为6个小时，当前不可配置）。在此期间，可以通过从回收站中移动文件来轻松恢复该文件。
2. 一旦回收站中保留文件的时间间隔到期，NameNode将从HDFS命名空间中删除该文件。
3. 释放组成已删除文件的块，并且系统显示增加的可用空间。

文件的复制因子不是静态的而是可以减少的。该信息通过下一个心跳消息传递到NameNode。然后，DataNode主动从其本地存储中删除该块，从而为群集提供更多空间。因此，NameNode主动维护每个文件的复制因子。

## Ensuring HDFS Reliability
Hadoop和HDFS旨在抵抗故障。数据丢失可以通过两种方式发生：
- DataNode可能会失败：每个DataNode都会定期将心跳消息发送到NameNode（默认值为3秒）。如果NameNode在预定时间间隔内未收到心跳消息，则认为DataNode发生故障。此时，它会主动将丢失节点中存储的块（这个块来自于这个节点的复制品）到正常节点。这样可以主动维护复制因子。
- 数据可能由于称为“位腐烂”的现象而损坏：这是指代表“位”的小电荷散布开来而导致数据丢失的事件。由于“校验和”不匹配，只能在HDFS读取操作期间检测到此情况。如果该块的校验和不匹配，则因为认为该块已损坏而启动了重新复制，并且NameNode主动尝试恢复该块的复制计数。

# Secondary NameNode
现在，我们准备讨论Secondary NameNode。 该组件可能是Hadoop平台中最易被错误命名的组件。我们要注意Secondary NameNode不是故障转移节点。

之前已了解到NameNode将其所有元数据保留在内存中。 它首先从存储在NameNode本地文件系统中的fsimagefile中读取它。 在Hadoop系统操作过程中，对NameNode内容的更新将应用到内存中。 但是，为了确保不会丢失数据，这些编辑操作还将应用于称为“编辑”的本地文件。

fsimage文件实际上并不存储块的位置。 它在系统启动期间从每个DataNode获取此信息，并将其保存在内存中。

edits文件的目标是在系统运行期间保存更改记录。如果重新启动系统，则可以在重新启动期间将edits文件的内容转移到fsimage中。但是，这会减慢Hadoop的重启速度。因此，程序员创建Secondary NameNode来处理此问题。Secondary NameNode的作用是定期合并fsimage文件中edits文件的内容。为此，Secondary NameNode定期执行以下步骤：
1. 它要求主服务器滚过编辑文件，这将确保新编辑转到新文件。这个新文件称为edit .new。
2. Secondary NameNode向主节点请求fsimage文件和edits文件。
3. Secondary NameNode将fsimage文件和edits文件合并到新的fsimage文件中。
4. NameNode从Secondary NameNode接收新的fsimage文件，并用它替换旧文件，随后将edits文件替换为第一步中创建的edits.new文件的内容。
5. 更新fstime文件以记录发生检查点操作的时间。

现在应该清楚为什么NameNode是Hadoop 1.x中的单点故障。如果fsimage和edits files文件损坏，则HDFS系统中的所有数据都将丢失。因此，尽管DataNode可以简单地是带有JBOD的商用机器（这意味着“只是一堆磁盘”），但NameNode和Secondary NameNode必须连接到更可靠的存储（基于RAID），以确保不会丢失数据。前面提到的两个文件也必须定期备份。如果需要在备份上还原它们，则从现在到进行备份之前的所有更新都将丢失。下面总结了使NameNode支持HDFS的关键文件。
1. fsimage包含截至最后一个检查点的HDFS元数据的持久状态
2. edits包含自上一个检查点以来HDFS元数据的状态更改
3. fstime包含最后一个检查点的时间戳

## TaskTracker
运行在Hadoop群集的每个计算节点上的TaskTracker守护程序接受对单个任务（例如Map，Reduce和Shuffle操作）的请求。 每个TaskTracker均配置有一组插槽，通常将其设置为计算机上可用内核的总数。 当收到（来自JobTracker的）启动任务的请求时，TaskTracker会为该任务启动一个新的JVM。 可以重用JVM，但是很难获得此功能的实际使用示例。 Hadoop平台的大多数用户只是将其关闭。 根据TaskTracker的可用插槽数量为其分配任务（任务总数=正在运行的实际任务）。 TaskTracker负责将心跳消息发送到JobTracker。 这些消息除了告诉JobTracker运行状况良好之外，还告诉JobTracker可用插槽的数量。

## JobTracker
JobTracker守护程序负责启动和监视MapReduce作业。以下步骤详细介绍了该过程：
1. Job Tracker接收到作业请求。
2. 大多数MapReduce作业需要一个或多个输入目录。Job Tracker向NameNode请求一个DataNodes列表，该DataNodes托管输入目录列表中包含的文件的块。
3. JobTracker现在计划执行作业。在此步骤中，JobTracker确定执行作业所需的任务数（Map任务和Reduce任务）。它还尝试将任务安排在尽可能靠近数据块的位置。
4. JobTracker将任务提交到每个TaskTracker节点以执行。监视TaskTracker节点的运行状况。它们以预定义的时间间隔将心跳消息发送到JobTracker节点。如果在预定义的时间内未收到心跳消息，则TaskTracker节点将被视为失败，并且将任务重新安排为在单独的节点上运行。
5. 完成所有任务后，JobTracker会将作业状态更新为成功。如果一定数量的任务反复失败（确切的数量是通过Hadoop配置文件中的配置指定的），则JobTracker会宣布作业失败。
6. 客户端轮询JobTracker以获取有关Job进度的更新。
到目前为止，有关Hadoop 1.x组件的讨论应该清楚地表明，即使JobTracker也是单点故障。如果JobTracker发生故障，则具有正在运行的作业的整个群集也会发生故障。另外，只有一个JobTracker，这会在同时运行多个作业的环境中增加单个JobTracker的负载。

# Hadoop 2.0
Hadoop 2.0，亦称为MapReduce 2.0（MR v2）或YARN。本书通常将版本称为2.x，因为预期该版本不会以任何根本方式改变行为和体系结构。MR v2是与MR v1兼容的应用程序编程接口（API），仅需重新编译即可。但是，基础体系结构已被彻底修改。在Hadoop 1.x中，JobScheduler具有两个主要功能：
- 资源管理
- Job scheduling/job monitoring
YARN的目的是将这些功能分成单独的守护程序，要实现这个需要拥有一个全局资源管理器和一个per–application的应用程序主机。注意，我们提到的是应用程序，而不是工作。在新的Hadoop 2.x中，应用程序可以是传统MapReduce作业中的单个作业，也可以是有向非循环图（DAG）
的工作。 DAG作业表示彼此之间具有层次关系的作业。

YARN还旨在将Hadoop的实用程序扩展到MapReduce之外。在以下各章中，我们将发现MapReduce框架的各种局限性。为了解决这些局限性，已经开发了更新的框架。例如，Apache Hive带来了Hadoop之上的SQL特性，Apache PIG解决了基于脚本、数据流风格处理的问题。即使是更新的框架，如Apache HAMA，也会处理迭代计算，这在机器学习风格的用例中非常典型。

Spark/Shark框架是Hive和HAMA之间的交叉，提供低延迟的SQL访问以及一些内存计算。尽管这些框架都设计为在HDFS上工作，但并不是所有的框架都是Hadoop框架的一等公民。我们需要的是一个总体框架,该框架可以支持具有不同计算原理的更新框架（不仅是MapReduce模型），例如基于HAMA的批量同步并行（BSP）模型或基于HAMA的内存中缓存和计算模型。新框架应从头开始设计，以支持新类型的应用程序，同时仍在整个Hadoop系统中运行。即使所有系统共享相同的基础HDFS，这也将使围绕安全性和资源管理的系统范围的策略得以一致地应用。

YARN系统具有以下组件：
- Global Resource Manager
- Node Manager
- Application-specific Application Master
- Scheduler
- Container

Container包括CPU内核总数和主内存大小的子集。应用程序将在一组Container中运行。 Application Master实例将向Global Resource Manager请求资源。Scheduler将通过每个节点的Node Manager分配资源（容器）。然后，Node Manager将向Resource Manager报告各个容器的使用情况。
Global Resource Manager和每个节点的Node Manager构成了新MapReduce框架的管理系统。Resource Manager是分配资源的最终权限。每种应用程序类型都有一个应用程序主机。 （例如，MapReduce是一种类型，每个MapReduce作业都是MapReduce类型的实例，类似于面向对象编程中的类和对象关系）。对于应用程序类型的每个应用程序，将实例化一个Application Master实例。 Application Master实例与Resource Manager协商Container以执行作业。Resource Manager与每个节点的Node Manager一起使用调度程序（全局组件）来分配这些资源。从系统角度来看，Application Master也可以在Container中运行。

MapReduce v1框架已被重用，没有进行任何重大修改，这将使它与现有MapReduce程序向后兼容。

# Components of YARN 
让我们更详细地讨论每个组件。 在较高级别上，我们在Hadoop集群中设置了一堆商用计算机，每台机器称为一个节点。
## Container
Container是YARN框架中的计算单元。它是一个工作单元所在的子系统。或者，使用MapReduce v1的语言，它是等效于任务的组件。Container与节点之间的关系是这样的：一个节点运行多个Container，但是一个Container不能越过节点边界。Container是一组分配的系统资源。当前仅支持两种类型的系统资源：
- CPU core
- Memory in MB
包含资源的Container将在某个节点上执行，因此Container中隐含的是“资源名称”的概念，即Container运行的机架和节点的名称。当请求一个容器时，它是在一个特定的节点上被请求的。因此，容器是授予应用程序在特定主机上使用特定数量的CPU内核和特定数量的内存的权利。任何作业或应用程序（单个作业或作业DAG）本质上都将在一个或多个Container中运行。最终负责物理分配容器的YARN框架实体称为节点管理器。
## Node Manager
节点管理器在群集中的单个节点上运行，并且群集中的每个节点都运行自己的节点管理器。它是一个从属服务：它接收来自另一个称为资源管理器的组件的请求，并将Container分配给应用程序。它还负责监视使用情况度量标准并将其报告给资源管理器。节点管理器与资源管理器一起构成了负责管理Hadoop集群上的资源分配的框架。资源管理器是一个全局组件，而节点管理器是一个按节点的代理，负责管理Hadoop集群中各个节点的运行状况。节点管理器的任务包括：
1. 从资源管理器接收请求，并代表作业分配Container。
2. 与资源管理器交换消息，以确保整个群集的平稳运行。资源管理器基于从每个节点管理器收到的报告来跟踪全局运行状况，该报告被委派了监视和管理其自身运行状况的任务。
3. 管理每个已启动Container的生命周期。
4. 每个节点上的日志管理。
5. 执行各种YARN应用程序利用的辅助服务。例如，MapReduce中的Shuffle服务在当前Hadoop实现中作为辅助服务实现。

节点启动时，它将向资源管理器注册并告诉资源管理器有多少资源（最终分配给表单容器）可用。在运行时，随着节点管理器和资源管理器一起工作，此信息将不断更新，以确保功能齐全且利用率最佳的群集。

节点管理器仅负责管理容器的抽象概念。 它不包含有关单个应用程序或应用程序类型的任何知识。 将此责任委托给一个称为“Application Master”的组件。 但是在讨论Application Master之前，让我们简要地访问资源管理器（Resource Manager）。

## Resource Manager
Resource Manager主要是一个调度程序：它在竞争的应用程序之间仲裁资源，以确保最佳的群集利用率。Resource Manager具有一个可插拔的调度程序，该调度程序负责按照各种常见的Container和队列约束，将资源分配给各种正在运行的应用程序。 调度程序的示例包括Hadoop中的Capacity Scheduler和Fair Scheduler，我们将在随后的章节中同时遇到这两者。创建、提供和监视资源的实际任务委托给每个节点Node Manager。这种关注点的分离使得Resource Manager比传统的JobScheduler可扩展得更多。

## Application Master
Application Master是旧版MapReduce v1框架和YARN之间的主要区别。 Application Master是特定于框架的库的实例。它从Resource Manager协商资源，并与Node Manager一起获取这些资源并执行其任务。Application Master是从Resource Manager协商资源容器的组件。Application Master带给YARN框架的主要好处是：
- Improved scalability
- A more generic framework

在MapReduce v1中，JobTracker负责管理任务故障转移。 JobTracker还负责为工作分配资源。 v2中的可伸缩性得到了改善，因为Resource Manager（JobTracker的替代品）现在仅负责调度。管理作业或应用程序的任务在于Application Master。如果任务失败，Application Master将协商Resource Manager中的资源并尝试重新执行任务。

在MapReduce v1中，Hadoop框架仅支持MapReduce类型的作业，它不是通用框架。主要原因是诸如JobTracker和TaskTracker之类的关键组件是在设计中深深植根于Map和Reduce任务概念的基础上开发的。随着MapReduce受到越来越多的关注，人们发现使用MapReduce进行某些类型的计算是不切实际的。因此，开发了新框架，例如基于Apache HAMA和Apache Giraph的BSP框架。他们很好地完成了图形计算，并且与HDFS配合得很好。在撰写本文时，诸如Shark / Spark之类的内存中框架正逐渐受到关注。尽管它们也可以与HDFS很好地配合使用，但是由于它们是使用非常不同的计算原理设计的，因此它们不适合Hadoop1.x。

作为YARN的一部分在v2中引入Application Master方法将改变所有这一切。通过将各个设计理念嵌入到Application Master中，可以使多个框架共存于单个受管系统中。因此，尽管Hadoop / HAMA / Shark在Hadoop 1.x的同一HDFS上的单独管理的系统上运行，导致意外的系统和资源冲突，但它们现在可以在同一Hadoop 2.x系统中运行。他们都将从Resource Manager中仲裁资源。 YARN将使Hadoop系统变得更加普及。 Hadoop现在将不仅支持MapReduce风格的计算，而且可插拔性更高：如果发现新系统可以更好地与某些类型的计算配合使用，则可以开发其应用程序母版并将其插入Hadoop系统。现在，Application Master概念允许Hadoop扩展到MapReduce之外，并使MapReduce与其他框架共存并合作。

# Anatomy of a YARN Request
当用户向Hadoop 2.x框架提交作业时，底层的YARN框架将处理请求。以下是使用的步骤：
1. 客户程序提交申请。还指定了反过来决定Application Master的应用程序类型。
2. Resource Manager协商资源以获取节点上的Container以启动Application Master的实例。
3. Application Master在Resource Manager中注册。通过此注册，客户端可以查询Resource Manager以获取有关Application Master的详细信息。因此，客户机将通过自己的Resource Manage与它启动的Application Master进行通信。
4. 在运行期间，Application Master通过资源请求从Resource Manager协商资源。资源请求还包括在其上请求Container的节点以及Container的规范（CPU代码和内存规格）。
5. 在启动的Container中执行的应用程序代码通过特定于应用程序的协议将其进度报告给Application Master（可能是远程的）。
6. 客户端程序通过特定于应用程序的协议与Application Master进行通信。客户端通过查询在步骤3中向其注册的Resource Manager来引用应用程序主机。
