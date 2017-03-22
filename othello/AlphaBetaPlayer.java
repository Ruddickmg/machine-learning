package othello;

import static othello.State.*;
import static othello.StdDraw.*;
import static java.lang.Math.*;
import java.util.*;

public class AlphaBetaPlayer implements Player {

	private int depth;

	public AlphaBetaPlayer (int d) {
		depth = d;
	}

	private int alphaBeta (State state, int idepth, double prevNeg, double prevPos, boolean isMax) {
		
		List<Integer> moves = state.legalMoves();
		int tscore, score = 0, move;
		State copy;

		if (idepth <= 0 || moves.get(0) < 0)

			score = state.score();

		else while (!moves.isEmpty()) {

			copy = state.copy();
			copy.play(moves.remove(0));

			tscore = alphaBeta(copy, idepth - 1, prevNeg, prevPos, !isMax);

			if (isMax) {
				if (tscore > score) {
					score = tscore;
					prevNeg = score;
				}
			} else if (tscore < score){
				score = tscore;
				prevPos = score;
			}

			if (prevPos <= prevNeg)
				break;
		}
		return score * (isMax ? 1 : -1);
	}

	private int alphaBeta(State state) {
		return alphaBeta(
			state, 
			depth, 
			Double.NEGATIVE_INFINITY, 
			Double.POSITIVE_INFINITY, 
			state.getColorToPlay() == 'X'
		);
	}

	/** Returns a legal move (0-63 or State.PASS) from state. */	
	public int move(State state) {

		int result = PASS, move = PASS, tscore;
		double score = Double.NEGATIVE_INFINITY;
		State copy;
		List<Integer> m = state.legalMoves();

		while (!m.isEmpty()) {

			copy = state.copy();
			move = m.remove(0);
			copy.play(move);

			tscore = alphaBeta(copy);

			if (tscore >= score && move >= 0) {
				result = move;
				score = tscore;
			}
		}
		return result;
	}

	public String toString() {
		return "AlphaBeta";
	}
} 