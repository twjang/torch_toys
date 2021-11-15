#include <torch/extension.h>
#include <string>
#include <assert.h>

namespace torch_toys {

class MNKTicTacToe {
protected:
    std::string board_;
    int m_;
    int n_;
    int k_;
public:
    MNKTicTacToe(std::string board, int m, int n, int k)
        :board_(board), m_(m), n_(n), k_(k) 
    { 
        assert(m_ > 0);
        assert(n_ > 0);
        assert(k_ > 0);
        assert(m_ >= k_);
        assert(n_ >= k_);
        assert(board_.length() == m_ * n_);
    }

    void set_board(std::string board) {
        board_ = board;
    }

    const std::string get_board() {
        return board_;
    }

    int height() const {
        return m_;
    }

    int width() const {
        return n_;
    }

    int win_length() const {
        return k_;
    }

    inline char at(int i, int j) const {
        if (i < -m_ || i >= m_) return ' ';
        if (j < -n_ || j >= n_) return ' ';
        if (i < 0) i += m_;
        if (j < 0) j += n_;
        int idx = i * m_ + j;

        char res = board_[idx];
        if (res < 'a' && res != ' ') res += ('a' - 'A');
        return res;
    }

    char winner() const {
        // -
        for (int i=0; i<m_; i++) { 
            int x_cnt = 0;
            int o_cnt = 0;

            for (int j=0; j<n_; j++) {
                char cur_checker = at(i, j);
                if (cur_checker == 'x') { 
                    o_cnt = 0;
                    x_cnt ++;
                } else if (cur_checker == 'o') {
                    x_cnt = 0;
                    o_cnt ++;
                } else {
                    x_cnt = 0;
                    o_cnt = 0;
                }

                if (o_cnt == k_) return 'o';
                else if (x_cnt == k_) return 'x';
            }
        }

        // |
        for (int j=0; j<n_; j++) {
            int x_cnt = 0;
            int o_cnt = 0;

            for (int i=0; i<m_; i++) { 
                char cur_checker = at(i, j);
                if (cur_checker == 'x') { 
                    o_cnt = 0;
                    x_cnt ++;
                } else if (cur_checker == 'o') {
                    x_cnt = 0;
                    o_cnt ++;
                } else {
                    x_cnt = 0;
                    o_cnt = 0;
                }

                if (o_cnt == k_) return 'o';
                else if (x_cnt == k_) return 'x';
            }
        }

        // \ /
        for (int dir=-1; dir < 2; dir += 2) {
            int i_end = m_ - k_;
            int j_end = n_ - k_;

            for (int i = 0; i <= i_end; i++) {
                for (int j = 0; j <= j_end; j++) {
                    int x_cnt = 0;
                    int o_cnt = 0;

                    for (int off = 0; off < k_; off++) {
                        int ci, cj;
                        if (dir > 0) {
                            ci = i + off;
                            cj = j + off;
                        } else {
                            ci = i - off + k_ - 1;
                            cj = j + off;
                        }

                        char cur_checker = at(ci, cj);
                        if (cur_checker == 'x') { 
                            o_cnt = 0;
                            x_cnt ++;
                        } else if (cur_checker == 'o') {
                            x_cnt = 0;
                            o_cnt ++;
                        } else {
                            x_cnt = 0;
                            o_cnt = 0;
                        }

                        if (o_cnt == k_) return 'o';
                        else if (x_cnt == k_) return 'x';
                    }
                }
            }
        }

        return ' ';
    }
};

std::string tictactoe_winner(const std::string board, int m, int n, int k) {
    const MNKTicTacToe game(board, m, n, k);
    std::string res = " ";
    res[0] = game.winner();
    return res;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("tictactoe_winner", &tictactoe_winner, "tictactoe_winner");
}

}