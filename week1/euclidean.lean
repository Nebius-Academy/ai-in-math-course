import Init.Data.Nat.Basic
import Init.Data.Nat.Gcd
import Init.Tactics

/-- Euclidean algorithm (our own), recursive on the first argument. -/
def euclidGcd (m n : Nat) : Nat :=
  match m with
  | 0     => n
  | m + 1 => euclidGcd (n % (m + 1)) (m + 1)
termination_by m
decreasing_by
  simp_wf
  exact Nat.mod_lt _ (Nat.succ_pos _)

/-- One-step unfolding lemmas (crucial: `rfl` won't work for well-founded recursion). -/
theorem euclidGcd_zero (n : Nat) : euclidGcd 0 n = n := by
  simp [euclidGcd]

theorem euclidGcd_succ (m n : Nat) :
    euclidGcd (m + 1) n = euclidGcd (n % (m + 1)) (m + 1) := by
  simp [euclidGcd]

/-- Correctness: our Euclid implementation computes the same thing as `Nat.gcd`. -/
theorem euclidGcd_eq_gcd (m n : Nat) : euclidGcd m n = Nat.gcd m n := by
  -- Use the Euclidean induction principle for `Nat.gcd`.
  refine Nat.gcd.induction (m := m) (n := n)
    (P := fun m n => euclidGcd m n = Nat.gcd m n)
    (H0 := ?base) (H1 := ?step)
  · intro n
    -- euclidGcd 0 n = gcd 0 n
    rw [euclidGcd_zero, Nat.gcd_zero_left]
  · intro m n hm ih
    -- hm : 0 < m, ih : euclidGcd (n % m) m = (n % m).gcd m
    cases m with
    | zero =>
        -- impossible: 0 < 0
        cases (Nat.lt_asymm hm hm)
    | succ k =>
        -- unfold BOTH sides exactly once, then it's literally ih
        rw [euclidGcd_succ, Nat.gcd_succ]
        exact ih


#eval euclidGcd 1071 462   -- should print 21


theorem gcd_1071_462 : Nat.gcd 1071 462 = 21 := by
  have h : euclidGcd 1071 462 = 21 := by
    native_decide
  exact (euclidGcd_eq_gcd 1071 462).symm.trans h
