import Mathlib.GroupTheory.SpecificGroups.Cyclic
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Algebra.Group.Subgroup.Finite
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.SetTheory.Cardinal.Finite

theorem isCyclic_of_prime_fintype_card
    (G : Type*) [Group G] [Fintype G]
    {p : ℕ} (hp : Fintype.card G = p) (pp : Nat.Prime p) :
    IsCyclic G := by
  classical

  -- Get a non-identity element since p is prime ⇒ p > 1
  have h1 : 1 < Fintype.card G := by
    simpa [hp] using pp.one_lt
  obtain ⟨g, hg⟩ := Fintype.exists_ne_of_one_lt_card h1 (1 : G)  -- g ≠ 1
  -- Fintype.exists_ne_of_one_lt_card

  -- Use: IsCyclic ↔ ∃ g, zpowers g = ⊤
  refine (isCyclic_iff_exists_zpowers_eq_top).2 ⟨g, ?_⟩
  -- isCyclic_iff_exists_zpowers_eq_top

  -- It suffices to show Nat.card (zpowers g) = Nat.card G
  apply Subgroup.eq_top_of_card_eq (H := Subgroup.zpowers g)
  -- Subgroup.eq_top_of_card_eq

  have hNatG : Nat.card G = p := by
    simp [Nat.card_eq_fintype_card, hp]
  -- Nat.card_eq_fintype_card

  have hzpow : Nat.card ↥(Subgroup.zpowers g) = orderOf g := by
    -- Fintype.card_zpowers has implicit {x : G}, so specify (x := g)
    simpa [Nat.card_eq_fintype_card] using (Fintype.card_zpowers (x := g))
  -- Fintype.card_zpowers

  have hdiv : orderOf g ∣ p := by
    have : orderOf g ∣ Fintype.card G := orderOf_dvd_card (x := g)
    -- orderOf_dvd_card
    simpa [hp] using this

  have hne1 : orderOf g ≠ 1 := by
    intro h
    have : g = 1 := (orderOf_eq_one_iff).1 h
    -- orderOf_eq_one_iff
    exact hg this

  have horder : orderOf g = p := by
    have : p = orderOf g := (Nat.Prime.dvd_iff_eq pp hne1).1 hdiv
    -- Nat.Prime.dvd_iff_eq
    exact this.symm

  calc
    Nat.card ↥(Subgroup.zpowers g) = orderOf g := hzpow
    _ = p := horder
    _ = Nat.card G := by simpa using hNatG.symm



theorem isCyclic_of_card_13
    (G : Type*) [Group G] [Fintype G]
    (h : Fintype.card G = 13) : IsCyclic G := by
  -- 13 is prime
  have hp13 : Nat.Prime 13 := by decide
  -- apply your general theorem with p := 13
  exact isCyclic_of_prime_fintype_card G (p := 13) h hp13
