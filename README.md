# reversi-mcts

Even though NaiveMCTS player has only very primitive policy but it played best
performance among the players so far.

||Random|Greedy|MinMax|NaiveMCTS|
|:--|:--|:--|:--|:--|
|**Random**   |0.|0.405|0.2|0.09|
|**Greedy**   |0.545|0.|0.5|0.035|
|**MinMAX**   |0.76|0.5|0.|0.085|
|**NaiveMCTS**|*0.895*|*0.965*|*0.915*|0.|

SimpleMCTS has been intoroduced. Any advantage of SimpleMCTS comparing to
NaiveMCTS for winning ratio cannot be seen.

Winning ratio @ 4x4 board:

||Random|Greedy|MinMax|NaiveMCTS|SimpleMCTS|
|:--|:--|:--|:--|:--|:--|
|**Random**   |0.|0.415|0.255|0.085|0.06|
|**Greedy**   |0.565|0.|0.5|0.045|0.08|
|**MinMAX**   |0.68|0.5|0.|0.12|0.215|
|**NaiveMCTS**|0.885|0.95|0.88|0.|0.53|
|**SimpleMCTS**|0.935|0.92|0.785|0.47|0.|
