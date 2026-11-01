/-
  Independent Lean 4 (core only, no Mathlib) formalisation for the audit.
  Generalises morpholib Theorem 3 (which is stated for one 4-element list and one
  3-element window) to EVERY list and EVERY position, and adds the witness that
  the neighbour ruler E can rise on a downhill swap.
  Check:  lean lean/AdjacentSwap.lean   (expect only the #print axioms lines)
-/
namespace Audit

def countLt (v : Nat) : List Nat → Nat
  | [] => 0
  | x :: xs => (if x < v then 1 else 0) + countLt v xs

/-- I(v): number of pairs i<j with v[i] > v[j]. -/
def inv : List Nat → Nat
  | [] => 0
  | x :: xs => countLt x xs + inv xs

/-- E(v): number of adjacent descents (upstream "monotonicity error"). -/
def desc : List Nat → Nat
  | [] => 0
  | [_] => 0
  | x :: y :: rest => (if y < x then 1 else 0) + desc (y :: rest)

/-- countLt is unchanged by swapping two adjacent entries anywhere in the list. -/
theorem countLt_swap (v b c : Nat) (pre post : List Nat) :
    countLt v (pre ++ c :: b :: post) = countLt v (pre ++ b :: c :: post) := by
  induction pre with
  | nil => simp only [List.nil_append, countLt]; omega
  | cons x xs ih => simp only [List.cons_append, countLt]; omega

/-- General theorem: an adjacent swap of a strictly inverted pair (b > c), at any
    position of any list, lowers I by exactly one. -/
theorem inv_adjacent_swap (b c : Nat) (pre post : List Nat) (h : c < b) :
    inv (pre ++ c :: b :: post) + 1 = inv (pre ++ b :: c :: post) := by
  induction pre with
  | nil =>
    simp only [List.nil_append, inv, countLt]
    have h1 : ¬ (b < c) := by omega
    simp only [h, h1, ite_true, ite_false]
    omega
  | cons x xs ih =>
    simp only [List.cons_append, inv]
    have hc := countLt_swap x b c xs post
    omega

/-- Witness that the paper's ruler E can rise while I falls (Dietz Claim 2). -/
theorem ruler_witness :
    inv [2, 1, 4, 3] + 1 = inv [2, 4, 1, 3] ∧ desc [2, 1, 4, 3] = desc [2, 4, 1, 3] + 1 := by
  decide

/-- Non-adjacent swap of an inverted pair can lower I by MORE than one, so
    "ΔI = −1 on every single swap" is false once Selection's long-range swaps are included. -/
theorem long_swap_drops_three : inv [3, 2, 1] = 3 ∧ inv [1, 2, 3] = 0 := by decide

/-- Swapping a NON-inverted pair rightward raises I (relevant if a Selection cell's
    pointer has passed its own position). -/
theorem uphill_witness : inv [1, 5, 9] = 0 ∧ inv [9, 5, 1] = 3 := by decide

#print axioms inv_adjacent_swap
#print axioms ruler_witness
end Audit
