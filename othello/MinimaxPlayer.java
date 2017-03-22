package othello;

import static othello.State.*;
import static othello.StdDraw.*;
import static java.lang.Math.*;
import java.util.*;

public class MinimaxPlayer implements Player {

	private int depth;

	public MinimaxPlayer (int d) {
		
		depth = d;
	}

	private int minMax (State state, int idepth, boolean isMax) {
		
		List<Integer> moves = state.legalMoves();
		int tscore, score = 0, move;
		State copy;

		if (idepth <= 0 || moves.get(0) < 0)

			score = state.score();

		else while (!moves.isEmpty()) {

			copy = state.copy();
			copy.play(moves.remove(0));
			tscore = minMax(copy, idepth - 1, !isMax);

			if (isMax ? tscore > score : tscore < score) {
				score = tscore;
			}
		}
		return score * (isMax ? 1 : -1);
	}

	private int minMax (State state) {
		return minMax(state, depth, state.getColorToPlay() == 'X');
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

			tscore = minMax(copy);

			if (tscore >= score && move >= 0) {
				result = move;
				score = tscore;
			}
		}
		return result;
	}

	public String toString() {
		return "Minimax";
	}
} 