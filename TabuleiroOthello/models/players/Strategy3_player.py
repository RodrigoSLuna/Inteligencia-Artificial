INFINITY = 10000000
#cantos, posicoes boas para cantos


class Strategy_3():
	bad_corners = [ [1,2],[2,1],[2,2],
					[1,7],[2,7],[2,8],
					[7,1],[7,8],[8,7],
					[7,7],[7,8],[8,7]         ]
	corners = [ [1 , 1],[ 1, 8], [8,1], [8,8] ]

	all_corners = [[1 , 1],[ 1, 8], [8,1], [8,8],
		   [1 , 3],[ 2 ,3],	[3,1], [3,2], [3,3],
		   [1 , 6],[ 2 ,6], [3,6], [3,7], [3,8],
		   [6 , 1],[ 6 ,2], [6,3], [7,3], [8,3],
		   [6 , 6],[ 6 ,7], [6,8], [7,6], [8,6]  ]
	corners_neighbors = [ [ 1 , 2 ],[ 2 ,1 ],[ 2, 2 ],
					  [  1, 7 ],[ 2 ,7 ],[ 2, 8 ],
					  [  7, 1 ],[ 7 ,2 ],[ 8, 2 ],
					  [  7, 7 ],[ 7 ,8 ],[ 8, 7]  ]  



	di = [-1 , -1, -1,  0, 0,  1, 1, 1]
	dj = [-1 ,  0,  1, -1, 1, -1, 0, 1]
	def __init__(self, color):
		self.color = color
		if self.color == '@':
			self.tipo = 1
		else:
			self.tipo = 0
	def play(self, board):									#alfa     #Beta
		Score,move = self.minimax(board,board,True,0, self.color,-INFINITY,INFINITY ) 
		return move


	def Pontuacao_Board(self, board,color ):
		soma = 0
		for moves in board.valid_moves(color):
			if [moves.x,moves.y] in self.all_corners:
				soma += 5
			elif [moves.x,moves.y] in self.corners_neighbors: 
				soma += -2
			else:
				soma += 2
		return soma

	def Total_Moves(self, board, color  ):
		return len( board.valid_moves(color) )



	def Stable_Adj(self, move, board ,color ):
		
		import Queue
		qtd = 0
		mrc = []
		mrc.append( move )
		q = Queue.Queue()
		q.put( move )

		while not q.empty():
			v = q.get()
			#print 'Entrou em LOOP'
			#print v
			for i in range(0,8):
				new_move_x = v[0] + self.di[i]
				new_move_y = v[1] + self.dj[i]

				if [new_move_x,new_move_y] in mrc:
					continue
				if board.board[ new_move_x ][ new_move_y ] != color:
					continue
				if board.board[ new_move_x ][ new_move_y ] == board.OUTER:
					continue
				#print board.board[new_move_x][new_move_y], color

				mrc.append( [new_move_x,new_move_y]  )
				q.put( [new_move_x,new_move_y ] )
				qtd += 1


		return 1+qtd



	def Stable_Moves(self, board, color  ):
		soma = 0 
		mrc = []
		for i in range(1,9):
			for j in range(1,9):
				if board.board[i][j] == color:
					if [i,j] in self.corners and [i,j] not in mrc:
						#soma += 5 + 3* self.Stable_Adj( [i,j],board,color )
						mrc.append([i,j])
						soma += 5
		return soma


	def Diff_Board( self,board_Inicial, board_Final, color, Op  ):

		#Cores, se for Preto e 1, senao 0.
		if color == '@':
			cor = 1
		else:
			cor = 0

		if Op == False:
			cor = (cor+1)%2

		Score_inicial = board_Inicial.score()
		Score_final   = board_Final.score()

		return Score_final[ cor ] - Score_inicial[ cor ]

	def Bad_Position(self, board,color):
		soma = 0
		for i in range(1,9):
			for j in range(1,9):
				if [i,j] in self.bad_corners and board.board[i][j] == color:
					
					for corner in self.corners:
						diff = i-corner[0] + j-corner[1]
						if board.board[ corner[0]  ][ corner[1] ] == board.EMPTY and diff <= 1 :
							soma -= 2

		return soma
	def minimax(self, board_inicial,board , Max ,Depth,color,alpha,beta):
		if Max:
			BetterScore = -INFINITY
		else:
			BetterScore = INFINITY
		if color == '@':
			next_color = 'o'
		else:
			next_color = '@'

		move        = self.getNearestCorner(board.valid_moves(color) )
		#Retorna o valor encontrado quando chegar numa folha
		#Volta da recurssao, avaliacao do no.
		if Depth == 4:
			Pontuacao_BOARD  = (self.Pontuacao_Board( board, color  )- self.Pontuacao_Board(board,next_color) )
			Pontuacao_STABLE = (self.Stable_Moves(board,color) - self.Stable_Moves(board,next_color)  )
			Pontuacao_MOVES  = (self.Total_Moves( board,color ) - self.Total_Moves( board , next_color ) )

			Pontuacao_DIFF   = (self.Diff_Board( board_inicial , board , self.color,True  ) ) - ( self.Diff_Board( board_inicial , board , self.color,False  ) ) 
			Pontuacao_BAD    = (self.Bad_Position(board,color))
			
			return Pontuacao_BOARD+ 10*Pontuacao_STABLE+ 3*Pontuacao_MOVES+ 0.1*Pontuacao_DIFF + 5*Pontuacao_BAD  ,self.getNearestCorner(board.valid_moves(color) )

		for moves in board.valid_moves(color):
			x,y = moves.x,moves.y
			Board_Aux = board.get_clone()
			Board_Aux.board[x][y] = color

			if Max:
				Next_Score,Better_Move =  self.minimax( board_inicial ,Board_Aux , False , Depth+1, next_color,alpha,beta   )
				
				if Next_Score > BetterScore:
					BetterScore = Next_Score
					move = moves
				alpha = max(alpha,BetterScore)

				if(beta <= alpha):
					break
			else:
				Next_Score,Better_move  =   self.minimax( board_inicial ,Board_Aux , True , Depth+1, next_color,alpha,beta   )
				if Next_Score < BetterScore:
					BetterScore = Next_Score
					move = moves
				beta = min(beta,BetterScore)

				if( beta <= alpha):
					break


		return BetterScore,move

	def getNearestCorner(self, moves):
		import math
		#Distancia minima.
		minDist = 10
		retMove = None
		for move in moves:
			for corner in self.corners:
				distX = abs(corner[0] - move.x)
				distY = abs(corner[1] - move.y)
				dist  = math.sqrt(distX*distX + distY*distY)
				if dist < minDist:
					minDist = dist
					retMove = move

		return retMove
