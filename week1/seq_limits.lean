import Mathlib

/-- ε–N definition: `SeqLimit u L` means `u n → L` as `n → ∞`. -/
def SeqLimit (u : ℕ → ℝ) (L : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ N : ℕ, ∀ n : ℕ, N ≤ n → |u n - L| < ε
-- ∀ ε : hε → ∃ N: hN

/-- Squeeze theorem (ε–N version):
if `aₙ ≤ bₙ ≤ cₙ` and `aₙ → L` and `cₙ → L`,
then `bₙ → L`. -/
theorem seqLimit_of_sandwich
    {a b c : ℕ → ℝ} {L : ℝ}
    (ha : SeqLimit a L)
    (hc : SeqLimit c L)
    (hab : ∀ n, a n ≤ b n)
    (hbc : ∀ n, b n ≤ c n) :
    SeqLimit b L := by

  -- Take some ε; hε extracts the condition 0 < ε
  intro ε hε
  -- From now on, our **goal** is to prove:
  --   ∃ N : ℕ, ∀ n : ℕ, N ≤ n → |u n - L| < ε

  -- Extract N1 and N2 (with their conditions) from ha and hc
  -- hN1 is ∀ n : ℕ, N1 ≤ n → |u n - L| < ε
  -- hN2 is ∀ n : ℕ, N2 ≤ n → |u n - L| < ε
  rcases ha ε hε with ⟨N1, hN1⟩
  rcases hc ε hε with ⟨N2, hN2⟩

  -- Refine means here:
  -- Our goal (∃ N:...) is achieved by max(N1,N2)
  -- But there's a hole in the proof, and we'll cover it
  -- Now we owe the proof that this witness works
  refine ⟨Nat.max N1 N2, ?_⟩
  -- From now on, our **goal** is hN: ∀ n : ℕ, N ≤ n → |u n - L| < ε
  --                                    n : hN       → **next goal**

  -- take n in ℕ, N ≤ n
  intro n hn
  -- The new **goal** is |u n - L| < ε

  -- le_trans is transitivity of inequality
  -- le_trans composes
  --    (Nat.le_max_left  N1 N2) means (N1 ≤ max(N1, N2)
  --    hn means (N ≤ n)
  -- Together they give N1 ≤ N
  have hn1 : N1 ≤ n := le_trans (Nat.le_max_left  N1 N2) hn
  --  Gives N2 ≤ N
  have hn2 : N2 ≤ n := le_trans (Nat.le_max_right N1 N2) hn

  -- Denote by haε the statement "|a n - L| < ε"
  -- which is proved by combination of:
  --     hn1: N1 ≤ n
  --     (hN1 n): ∀ (n : ℕ), N1 ≤ n → |a n - L| < ε,
  --         applied for particular n
  have haε : |a n - L| < ε := hN1 n hn1
  have hcε : |c n - L| < ε := hN2 n hn2

  -- From |a n - L| < ε, get L - ε < a n
  have ha_lower : L - ε < a n := by
    have : -ε < a n - L := (abs_lt.mp haε).1
    linarith

  -- From |c n - L| < ε, get c n < L + ε
  have hc_upper : c n < L + ε := by
    have : c n - L < ε := (abs_lt.mp hcε).2
    linarith
  -- linarith is the “linear arithmetic” tactic:
  -- it tries to solve goals
  -- using only linear equalities/inequalities

  -- (lt_of_lt_of_le (huv : u < v) (hbc : v ≤ w)) means:
  --     If u < v and v ≤ w, then u < w.
  -- Here:
  --     huv is ha_lower := L - ε < a n
  --     hvw is (hab n) := (∀ n, a n ≤ b n) for the particular n
  have hb_lower : L - ε < b n := lt_of_lt_of_le ha_lower (hab n)
  have hb_upper : b n < L + ε := lt_of_le_of_lt (hbc n) hc_upper

  -- Turn (L - ε < b n) and (b n < L + ε) into |b n - L| < ε
  have hb1 : -ε < b n - L := by linarith
  have hb2 : b n - L < ε := by linarith
  -- Exact says: the goal is exactly: ...
  -- abs_lt.mpr means: |u| < v iff -v < u ∧ u < v
  exact (abs_lt.mpr ⟨hb1, hb2⟩)

#check SeqLimit
#print SeqLimit
