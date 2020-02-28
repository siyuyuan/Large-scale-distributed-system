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

在很长一段时间内，Hadoop仍然是一个用户提交作业的系统，这些作业运行在整个集群上。作业将在先进先出模式下执行。然而，这导致了这样一种情况：一项长期的、不那么重要的工作会占用资源，而不允许执行一项较小但更重要的工作。为了解决这个问题，为了解决此问题，在Hadoop中创建了更复杂的作业调度程序，例如Fair Scheduler和Capacity Scheduler。但是Hadoop1.x（在0.23版本之前）仍然存在可伸缩性限制。

